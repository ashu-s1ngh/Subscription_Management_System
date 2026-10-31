from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import (
    auth, products, plans, customers, quotations,
    subscriptions, invoices, payments, discounts, analytics, staff
)
from app.core.config import settings

app = FastAPI(
    title="Brightloop API",
    description="Subscription & Recurring Billing Management Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["Plans"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(quotations.router, prefix="/api/v1/quotations", tags=["Quotations"])
app.include_router(subscriptions.router, prefix="/api/v1/subscriptions", tags=["Subscriptions"])
app.include_router(invoices.router, prefix="/api/v1/invoices", tags=["Invoices"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(discounts.router, prefix="/api/v1/discounts", tags=["Discounts"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(staff.router, prefix="/api/v1/admin/staff", tags=["Staff Management"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "Brightloop API"}
