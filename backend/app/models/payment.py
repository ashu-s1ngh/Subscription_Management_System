from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentMethod(str, Enum):
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    OTHER = "other"

class PaymentCreate(BaseModel):
    invoice_id: str
    amount: float
    payment_method: PaymentMethod
    notes: Optional[str] = None

class PaymentResponse(PaymentCreate):
    id: str
    payment_date: datetime
