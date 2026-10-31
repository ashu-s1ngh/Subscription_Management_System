from __future__ import annotations

from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .mvp_models import *
from .store import ConflictError, NotFoundError, Store, store, today

app = FastAPI(title="Brightloop Subscription API", version="0.1.0", description="Business logic API for subscription billing.")
api = APIRouter(prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.FRONTEND_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_store() -> Store:
    return store


def require_role(x_role: str | None, allowed: set[Role]) -> None:
    role = Role(x_role or Role.staff)
    if role not in allowed:
        raise HTTPException(status_code=403, detail="This role cannot perform this action")


@app.exception_handler(NotFoundError)
async def not_found(_, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


def find_discount(code: str, db: Store) -> Discount | None:
    normalized = code.strip().upper()
    return next((item for item in db.discounts.values() if item.code == normalized), None)


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "brightloop-api"}


@api.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Product:
    require_role(x_role, {Role.admin})
    item = Product(**db.timestamps(), **payload.model_dump())
    db.products[item.id] = item
    return item


@api.get("/products", response_model=list[Product])
def list_products(db: Store = Depends(get_store)) -> list[Product]:
    return list(db.products.values())


@api.post("/plans", response_model=Plan, status_code=201)
def create_plan(payload: PlanCreate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Plan:
    require_role(x_role, {Role.admin})
    db.get(db.products, payload.product_id)
    item = Plan(**db.timestamps(), **payload.model_dump())
    db.plans[item.id] = item
    return item


@api.get("/plans", response_model=list[Plan])
def list_plans(db: Store = Depends(get_store)) -> list[Plan]:
    return list(db.plans.values())


@api.post("/customers", response_model=Customer, status_code=201)
def create_customer(payload: CustomerCreate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Customer:
    require_role(x_role, {Role.admin, Role.staff})
    if any(item.email == payload.email for item in db.customers.values()):
        raise HTTPException(status_code=409, detail="A customer with this email already exists")
    item = Customer(**db.timestamps(), **payload.model_dump())
    db.customers[item.id] = item
    return item


@api.get("/customers", response_model=list[Customer])
def list_customers(db: Store = Depends(get_store)) -> list[Customer]:
    return list(db.customers.values())


@api.post("/discounts", response_model=Discount, status_code=201)
def create_discount(payload: DiscountCreate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Discount:
    require_role(x_role, {Role.admin})
    if find_discount(payload.code, db):
        raise HTTPException(status_code=409, detail="Discount code already exists")
    item = Discount(**db.timestamps(), **payload.model_dump())
    db.discounts[item.id] = item
    return item


@api.post("/subscriptions", response_model=Subscription, status_code=201)
def create_subscription(payload: SubscriptionCreate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Subscription:
    require_role(x_role, {Role.admin, Role.staff})
    db.get(db.customers, payload.customer_id)
    plan = db.get(db.plans, payload.plan_id)
    if payload.discount_code and not find_discount(payload.discount_code, db):
        raise HTTPException(status_code=400, detail="Discount code is invalid or expired")
    start = payload.start_on or today()
    item = Subscription(**db.timestamps(), **payload.model_dump(exclude={"start_on"}, exclude_none=True), status=SubscriptionStatus.active, start_on=start, next_billing_on=start + timedelta(days=365 if plan.billing_interval == "yearly" else 30))
    db.subscriptions[item.id] = item
    return item


@api.get("/subscriptions", response_model=list[Subscription])
def list_subscriptions(customer_id: UUID | None = Query(None), db: Store = Depends(get_store)) -> list[Subscription]:
    items = list(db.subscriptions.values())
    return [item for item in items if customer_id is None or item.customer_id == customer_id]


@api.patch("/subscriptions/{subscription_id}/status", response_model=Subscription)
def transition_subscription(subscription_id: UUID, payload: SubscriptionStatusUpdate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Subscription:
    require_role(x_role, {Role.admin, Role.staff})
    item = db.get(db.subscriptions, subscription_id)
    allowed = {SubscriptionStatus.draft: {SubscriptionStatus.active, SubscriptionStatus.cancelled}, SubscriptionStatus.active: {SubscriptionStatus.paused, SubscriptionStatus.cancelled}, SubscriptionStatus.paused: {SubscriptionStatus.active, SubscriptionStatus.cancelled}, SubscriptionStatus.cancelled: set(), SubscriptionStatus.expired: set()}
    if payload.status not in allowed[item.status]:
        raise HTTPException(status_code=409, detail=f"Cannot transition subscription from {item.status} to {payload.status}")
    item.status = payload.status
    if payload.status == SubscriptionStatus.cancelled:
        item.cancelled_on = today()
    return db.touch(item)


@api.post("/subscriptions/{subscription_id}/invoice", response_model=Invoice, status_code=201)
def generate_invoice(subscription_id: UUID, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Invoice:
    require_role(x_role, {Role.admin, Role.staff})
    subscription = db.get(db.subscriptions, subscription_id)
    plan = db.get(db.plans, subscription.plan_id)
    discount_amount = Decimal("0")
    if subscription.discount_code:
        discount = find_discount(subscription.discount_code, db)
        if discount:
            discount_amount = plan.price * discount.value / 100 if discount.discount_type == DiscountType.percentage else min(discount.value, plan.price)
    subtotal = plan.price
    taxable = subtotal - discount_amount
    tax = (taxable * Decimal("0.18")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = taxable + tax
    invoice = Invoice(**db.timestamps(), subscription_id=subscription.id, customer_id=subscription.customer_id, number=f"INV-{len(db.invoices) + 1:05d}", status=InvoiceStatus.issued, due_on=today() + timedelta(days=7), subtotal=subtotal, discount=discount_amount, tax=tax, total=total, lines=[InvoiceLine(description=plan.name, quantity=1, unit_price=plan.price, subtotal=plan.price)])
    db.invoices[invoice.id] = invoice
    return invoice


@api.get("/invoices", response_model=list[Invoice])
def list_invoices(customer_id: UUID | None = Query(None), db: Store = Depends(get_store)) -> list[Invoice]:
    return [item for item in db.invoices.values() if customer_id is None or item.customer_id == customer_id]


@api.post("/payments", response_model=Payment, status_code=201)
def record_payment(payload: PaymentCreate, db: Store = Depends(get_store), x_role: str | None = Header(None)) -> Payment:
    require_role(x_role, {Role.admin, Role.staff})
    invoice = db.get(db.invoices, payload.invoice_id)
    if invoice.status in {InvoiceStatus.paid, InvoiceStatus.void}:
        raise HTTPException(status_code=409, detail="Invoice cannot accept a payment")
    if payload.amount != invoice.total:
        raise HTTPException(status_code=400, detail=f"Payment must equal invoice total ({invoice.total})")
    payment = Payment(**db.timestamps(), **payload.model_dump(), status=PaymentStatus.succeeded)
    db.payments[payment.id] = payment
    invoice.status = InvoiceStatus.paid
    invoice.paid_at = payment.created_at
    db.touch(invoice)
    return payment


@api.get("/analytics", response_model=Analytics)
def analytics(db: Store = Depends(get_store)) -> Analytics:
    active = [item for item in db.subscriptions.values() if item.status == SubscriptionStatus.active]
    paid = [item for item in db.invoices.values() if item.status == InvoiceStatus.paid]
    outstanding = [item for item in db.invoices.values() if item.status in {InvoiceStatus.issued, InvoiceStatus.overdue}]
    mrr = sum((db.plans[item.plan_id].price for item in active), Decimal("0"))
    counts = {state.value: sum(item.status == state for item in db.subscriptions.values()) for state in SubscriptionStatus}
    return Analytics(active_subscriptions=len(active), monthly_recurring_revenue=mrr, total_revenue=sum((item.total for item in paid), Decimal("0")), outstanding_invoices=sum((item.total for item in outstanding), Decimal("0")), customers=len(db.customers), subscriptions_by_status=counts)


app.include_router(api)

