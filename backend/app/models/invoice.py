from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PAID = "paid"
    CANCELLED = "cancelled"

class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    subscription_id: Optional[str]
    customer_id: str
    status: InvoiceStatus
    billing_period_start: date
    billing_period_end: date
    subtotal: float
    tax: float
    discount: float
    total_amount: float
    paid_amount: float
    due_date: date
