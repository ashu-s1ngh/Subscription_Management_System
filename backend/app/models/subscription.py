from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class SubscriptionStatus(str, Enum):
    DRAFT = "draft"
    QUOTATION = "quotation"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"

class SubscriptionItemCreate(BaseModel):
    product_id: str
    variant_name: Optional[str] = None
    quantity: int = 1
    unit_price: float

class SubscriptionCreate(BaseModel):
    customer_id: str
    plan_id: str
    start_date: date
    expiry_date: Optional[date] = None
    payment_terms: str = "Due on receipt"
    items: List[SubscriptionItemCreate] = []

class SubscriptionResponse(BaseModel):
    id: str
    subscription_number: str
    customer_id: str
    plan_id: str
    status: SubscriptionStatus
    start_date: date
    expiry_date: Optional[date]
    total_amount: float
