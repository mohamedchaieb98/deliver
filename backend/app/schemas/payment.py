import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: float
    payment_method: str
    order_id: Optional[str] = None
    transaction_id: Optional[str] = None
    status: Optional[str] = "pending"
    processed_by: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    order_id: Optional[str] = None
    transaction_id: Optional[str] = None
    status: Optional[str] = None
    processed_by: Optional[str] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: uuid.UUID
    payment_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
