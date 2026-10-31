from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class BillingCycle(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class PlanCreate(BaseModel):
    product_id: str
    name: str
    price: float
    billing_cycle: BillingCycle
    min_quantity: int = 1
    availability_start: Optional[date] = None
    availability_end: Optional[date] = None
    auto_close: bool = False
    allow_early_closing: bool = True
    allow_pause: bool = True

class PlanResponse(PlanCreate):
    id: str
