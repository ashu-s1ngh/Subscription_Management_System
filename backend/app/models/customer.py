from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company_name: Optional[str] = None
    billing_address: Optional[str] = None

class CustomerResponse(CustomerCreate):
    id: str
    profile_id: Optional[str] = None
    created_at: datetime
