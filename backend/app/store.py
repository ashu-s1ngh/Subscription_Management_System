from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, TypeVar
from uuid import UUID, uuid4

from .core.config import settings
from .mvp_models import Customer, Discount, Invoice, Payment, Plan, Product, Subscription

logger = logging.getLogger(__name__)
T = TypeVar("T")


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class PersistentCollection(dict[UUID, T]):
    """Dictionary cache that mirrors writes to a Supabase table when enabled."""

    def __init__(self, table_name: str, persist: Callable[[str, T], None]) -> None:
        super().__init__()
        self.table_name = table_name
        self._persist = persist
        self.persistence_enabled = False

    def __setitem__(self, key: UUID, value: T) -> None:
        super().__setitem__(key, value)
        if self.persistence_enabled:
            self._persist(self.table_name, value)


class Store:
    """MVP repository with Supabase persistence and an offline memory fallback."""

    def __init__(self) -> None:
        self.client: Any | None = self._create_client()
        self.products: PersistentCollection[Product] = PersistentCollection("products", self._persist)
        self.plans: PersistentCollection[Plan] = PersistentCollection("plans", self._persist)
        self.customers: PersistentCollection[Customer] = PersistentCollection("customers", self._persist)
        self.discounts: PersistentCollection[Discount] = PersistentCollection("discounts", self._persist)
        self.subscriptions: PersistentCollection[Subscription] = PersistentCollection("subscriptions", self._persist)
        self.invoices: PersistentCollection[Invoice] = PersistentCollection("invoices", self._persist)
        self.payments: PersistentCollection[Payment] = PersistentCollection("payments", self._persist)

        if self.client is None:
            self.seed()
        else:
            self._load_remote()

        for collection in self._collections():
            collection.persistence_enabled = self.client is not None

    @staticmethod
    def timestamps() -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {"id": uuid4(), "created_at": now, "updated_at": now}

    def _collections(self) -> list[PersistentCollection[Any]]:
        return [self.products, self.plans, self.customers, self.discounts, self.subscriptions, self.invoices, self.payments]

    def _create_client(self) -> Any | None:
        placeholders = ("your-", "placeholder", "example.supabase.co")
        if any(value.lower().startswith(placeholders) for value in (settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)):
            return None
        try:
            from supabase import create_client

            return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        except Exception as exc:
            raise RuntimeError("Supabase credentials are configured, but the client could not be created") from exc

    def _load_remote(self) -> None:
        loaders = (
            ("products", self.products, self._product_from_row),
            ("plans", self.plans, self._plan_from_row),
            ("customers", self.customers, self._customer_from_row),
            ("discounts", self.discounts, self._discount_from_row),
            ("subscriptions", self.subscriptions, self._subscription_from_row),
            ("invoices", self.invoices, self._invoice_from_row),
            ("payments", self.payments, self._payment_from_row),
        )
        try:
            for table_name, collection, converter in loaders:
                rows = self.client.table(table_name).select("*").execute().data or []
                for row in rows:
                    item = converter(row)
                    dict.__setitem__(collection, item.id, item)
        except Exception as exc:
            raise RuntimeError("Supabase connection succeeded, but loading the Brightloop tables failed") from exc

    def _persist(self, table_name: str, item: T) -> None:
        if self.client is None:
            return
        payload = self._row_for(table_name, item)
        self.client.table(table_name).upsert(payload).execute()

        if table_name == "invoices" and isinstance(item, Invoice):
            self.client.table("invoice_items").delete().eq("invoice_id", str(item.id)).execute()
            lines = [
                {
                    "invoice_id": str(item.id),
                    "description": line.description,
                    "quantity": line.quantity,
                    "unit_price": str(line.unit_price),
                    "total_price": str(line.subtotal),
                }
                for line in item.lines
            ]
            if lines:
                self.client.table("invoice_items").insert(lines).execute()

    def get(self, collection: dict[UUID, T], item_id: UUID) -> T:
        try:
            return collection[item_id]
        except KeyError as exc:
            raise NotFoundError(f"Record {item_id} was not found") from exc

    def touch(self, item: T) -> T:
        if hasattr(item, "updated_at"):
            item.updated_at = datetime.now(timezone.utc)  # type: ignore[attr-defined]
        if self.client is not None:
            for collection in self._collections():
                if getattr(item, "id", None) in collection:
                    self._persist(collection.table_name, item)
                    break
        return item

    def seed(self) -> None:
        product = Product(**self.timestamps(), name="Brightloop Pro", description="All-in-one subscription plan")
        dict.__setitem__(self.products, product.id, product)
        plan = Plan(**self.timestamps(), product_id=product.id, name="Pro Monthly", price=Decimal("49.00"), billing_interval="monthly")
        dict.__setitem__(self.plans, plan.id, plan)

    @staticmethod
    def _product_from_row(row: dict[str, Any]) -> Product:
        return Product(
            id=UUID(str(row["id"])),
            created_at=row["created_at"],
            updated_at=row.get("updated_at") or row["created_at"],
            name=row["name"],
            description=row.get("description") or "",
            active=row.get("status", "active") == "active",
        )

    @staticmethod
    def _plan_from_row(row: dict[str, Any]) -> Plan:
        return Plan(id=UUID(str(row["id"])), created_at=row["created_at"], updated_at=row.get("created_at"), product_id=UUID(str(row["product_id"])), name=row["name"], price=Decimal(str(row["price"])), billing_interval="yearly" if row["billing_cycle"] == "yearly" else "monthly", trial_days=0, active=True)

    @staticmethod
    def _customer_from_row(row: dict[str, Any]) -> Customer:
        return Customer(id=UUID(str(row["id"])), created_at=row["created_at"], updated_at=row.get("updated_at") or row["created_at"], name=row["name"], email=row["email"], company=row.get("company_name"))

    @staticmethod
    def _discount_from_row(row: dict[str, Any]) -> Discount:
        return Discount(id=UUID(str(row["id"])), created_at=row["created_at"], updated_at=row["created_at"], code=row["code"], discount_type=row["type"], value=Decimal(str(row["value"])), expires_on=row.get("end_date"))

    def _subscription_from_row(self, row: dict[str, Any]) -> Subscription:
        plan = self.plans.get(UUID(str(row["plan_id"])))
        interval_days = 365 if plan and plan.billing_interval == "yearly" else 30
        start = row["start_date"]
        start_date = date.fromisoformat(start) if isinstance(start, str) else start
        return Subscription(id=UUID(str(row["id"])), created_at=row["created_at"], updated_at=row.get("updated_at") or row["created_at"], customer_id=UUID(str(row["customer_id"])), plan_id=UUID(str(row["plan_id"])), discount_code=None, start_on=start_date, next_billing_on=start_date + timedelta(days=interval_days), status="cancelled" if row["status"] == "closed" else row["status"])

    @staticmethod
    def _invoice_from_row(row: dict[str, Any]) -> Invoice:
        status = {"paid": "paid", "cancelled": "void"}.get(row["status"], "issued")
        return Invoice(id=UUID(str(row["id"])), created_at=row["created_at"], updated_at=row["created_at"], subscription_id=UUID(str(row["subscription_id"])), customer_id=UUID(str(row["customer_id"])), number=row["invoice_number"], status=status, due_on=row["due_date"], subtotal=Decimal(str(row["subtotal"])), discount=Decimal(str(row["discount"])), tax=Decimal(str(row["tax"])), total=Decimal(str(row["total_amount"])), lines=[])

    @staticmethod
    def _payment_from_row(row: dict[str, Any]) -> Payment:
        return Payment(id=UUID(str(row["id"])), created_at=row["payment_date"], updated_at=row["payment_date"], invoice_id=UUID(str(row["invoice_id"])), amount=Decimal(str(row["amount"])), provider=row["payment_method"], reference=row.get("notes"), status="succeeded")

    @staticmethod
    def _row_for(table_name: str, item: T) -> dict[str, Any]:
        if table_name == "products":
            return {
                "id": str(item.id),
                "name": item.name,
                "code": f"BL-{str(item.id).split('-')[0].upper()}",
                "category": "service",
                "description": item.description,
                "status": "active" if item.active else "inactive",
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat(),
            }
        if table_name == "plans":
            return {"id": str(item.id), "product_id": str(item.product_id), "name": item.name, "price": str(item.price), "billing_cycle": item.billing_interval, "min_quantity": 1, "allow_pause": True}
        if table_name == "customers":
            return {"id": str(item.id), "name": item.name, "email": item.email, "company_name": item.company}
        if table_name == "discounts":
            return {"id": str(item.id), "code": item.code, "type": item.discount_type.value, "value": str(item.value), "end_date": item.expires_on.isoformat() if item.expires_on else None}
        if table_name == "subscriptions":
            plan = item.plan_id
            return {"id": str(item.id), "subscription_number": f"SUB-{str(item.id)[:8].upper()}", "customer_id": str(item.customer_id), "plan_id": str(plan), "status": "closed" if item.status.value == "cancelled" else item.status.value, "start_date": item.start_on.isoformat(), "payment_terms": "Due on receipt", "total_amount": "0"}
        if table_name == "invoices":
            return {"id": str(item.id), "invoice_number": item.number, "subscription_id": str(item.subscription_id), "customer_id": str(item.customer_id), "status": "confirmed" if item.status.value == "issued" else item.status.value, "billing_period_start": item.created_at.date().isoformat(), "billing_period_end": item.due_on.isoformat(), "subtotal": str(item.subtotal), "tax": str(item.tax), "discount": str(item.discount), "total_amount": str(item.total), "paid_amount": str(item.total if item.status.value == "paid" else 0), "due_date": item.due_on.isoformat()}
        if table_name == "payments":
            return {"id": str(item.id), "invoice_id": str(item.invoice_id), "amount": str(item.amount), "payment_method": item.provider if item.provider in {"upi", "bank_transfer", "cash", "other"} else "other", "payment_date": item.created_at.isoformat(), "notes": item.reference}
        raise ValueError(f"Unsupported persistence table: {table_name}")


def today() -> date:
    return datetime.now(timezone.utc).date()


store = Store()
