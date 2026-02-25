from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class PaymentBase(BaseModel):
    order_id: Optional[uuid.UUID] = None
    amount: float
    payment_method: str
    transaction_id: Optional[str] = None
    status: Optional[str] = "pending"
    processed_by: Optional[uuid.UUID] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    order_id: Optional[uuid.UUID] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    status: Optional[str] = None
    processed_by: Optional[uuid.UUID] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: uuid.UUID
    payment_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
