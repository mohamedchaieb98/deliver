import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class ExpenseBase(BaseModel):
    description: str
    amount: float
    expense_date: date
    status: Optional[str] = "pending"
    # deliverer_id: Optional[uuid.UUID] = None
    receipt_photo_path: Optional[str] = None
    location: Optional[str] = None
    is_reimbursable: Optional[bool] = True


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    status: Optional[str] = None
    # deliverer_id: Optional[uuid.UUID] = None
    receipt_photo_path: Optional[str] = None
    location: Optional[str] = None
    is_reimbursable: Optional[bool] = None
    approved_by: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None


class ExpenseResponse(ExpenseBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    approved_by: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
