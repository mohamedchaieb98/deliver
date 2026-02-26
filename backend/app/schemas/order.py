from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class OrderItemBase(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    total_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: str
    order_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    order_number: str
    client_id: Optional[str] = None
    reseller_id: Optional[str] = None
    deliverer_id: Optional[str] = None
    status: Optional[str] = "pending"
    order_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    delivery_address: Optional[str] = None
    total_amount: float
    notes: Optional[str] = None

    @validator("order_date", "delivery_date", pre=True)
    def parse_dates(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                try:
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    return None
        return v


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    client_id: Optional[str] = None
    reseller_id: Optional[str] = None
    deliverer_id: Optional[str] = None
    status: Optional[str] = None
    order_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    delivery_address: Optional[str] = None
    total_amount: Optional[float] = None
    notes: Optional[str] = None
    items: Optional[List[OrderItemCreate]] = None

    @validator("order_date", "delivery_date", pre=True)
    def parse_dates(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                try:
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    return None
        return v


class OrderResponse(OrderBase):
    id: str
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
