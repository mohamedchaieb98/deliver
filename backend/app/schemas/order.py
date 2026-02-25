import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    order_number: str
    status: Optional[str] = "pending"
    reseller_id: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    status: Optional[str] = None
    reseller_id: Optional[str] = None


class OrderResponse(OrderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
