from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Role(StrEnum):
    admin = "admin"
    staff = "staff"
    customer = "customer"


class SubscriptionStatus(StrEnum):
    draft = "draft"
    active = "active"
    paused = "paused"
    cancelled = "cancelled"
    expired = "expired"


class InvoiceStatus(StrEnum):
    draft = "draft"
    issued = "issued"
    paid = "paid"
    overdue = "overdue"
    void = "void"


class PaymentStatus(StrEnum):
    succeeded = "succeeded"
    failed = "failed"


class DiscountType(StrEnum):
    percentage = "percentage"
    fixed = "fixed"


class Record(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=1000)
    active: bool = True


class Product(ProductCreate, Record):
    pass


class PlanCreate(BaseModel):
    product_id: UUID
    name: str = Field(min_length=2, max_length=120)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    billing_interval: str = Field(pattern="^(monthly|yearly)$")
    trial_days: int = Field(default=0, ge=0, le=365)
    active: bool = True


class Plan(PlanCreate, Record):
    pass


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=254)
    company: str | None = Field(default=None, max_length=160)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("email must contain a valid address")
        return value


class Customer(CustomerCreate, Record):
    pass


class DiscountCreate(BaseModel):
    code: str = Field(min_length=2, max_length=40)
    discount_type: DiscountType
    value: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    expires_on: date | None = None

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return value.strip().upper()


class Discount(DiscountCreate, Record):
    pass


class SubscriptionCreate(BaseModel):
    customer_id: UUID
    plan_id: UUID
    discount_code: str | None = None
    start_on: date | None = None


class Subscription(SubscriptionCreate, Record):
    status: SubscriptionStatus
    start_on: date
    next_billing_on: date
    cancelled_on: date | None = None


class SubscriptionStatusUpdate(BaseModel):
    status: SubscriptionStatus


class InvoiceLine(BaseModel):
    description: str
    quantity: int = Field(gt=0)
    unit_price: Decimal
    subtotal: Decimal


class Invoice(Record):
    subscription_id: UUID
    customer_id: UUID
    number: str
    status: InvoiceStatus
    due_on: date
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal
    lines: list[InvoiceLine]
    paid_at: datetime | None = None


class PaymentCreate(BaseModel):
    invoice_id: UUID
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    provider: str = Field(default="demo", max_length=40)
    reference: str | None = Field(default=None, max_length=120)


class Payment(Record):
    invoice_id: UUID
    amount: Decimal
    provider: str
    reference: str | None
    status: PaymentStatus


class Analytics(BaseModel):
    active_subscriptions: int
    monthly_recurring_revenue: Decimal
    total_revenue: Decimal
    outstanding_invoices: Decimal
    customers: int
    subscriptions_by_status: dict[str, int]


class ErrorResponse(BaseModel):
    detail: str


JSONValue = dict[str, Any]
