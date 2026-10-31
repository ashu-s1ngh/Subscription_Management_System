from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class DiscountType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"

class DiscountCreate(BaseModel):
    code: str
    type: DiscountType
    value: float
    min_purchase: float = 0.0
    min_quantity: int = 0
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    max_usage: int = 0

class DiscountResponse(DiscountCreate):
    id: str
    used_count: int
    is_active: bool
