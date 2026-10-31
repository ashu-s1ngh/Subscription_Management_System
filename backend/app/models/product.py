from pydantic import BaseModel
from typing import List, Optional, Any

class ProductVariant(BaseModel):
    name: str
    price_adjustment: float = 0.0

class ProductCreate(BaseModel):
    name: str
    type: str = "service"
    sales_price: float
    cost_price: float = 0.0
    description: Optional[str] = None
    variants: List[ProductVariant] = []

class ProductResponse(ProductCreate):
    id: str
    is_active: bool = True
