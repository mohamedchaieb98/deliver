from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

# Base schema with common fields
class ResellerBase(BaseModel):
    business_name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

# Schema for creating a new reseller
class ResellerCreate(ResellerBase):
    pass

# Schema for updating a reseller (all fields optional)
class ResellerUpdate(BaseModel):
    business_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for API responses
class ResellerResponse(ResellerBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True