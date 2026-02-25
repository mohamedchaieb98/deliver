from pydantic import BaseModel 
from typing import Optional
from datetime import datetime
import uuid


class InventoryBase(BaseModel):
    product_id: str
    quantity: int = 0
    reserved: int = 0
    location: Optional[str] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    is_active: bool = True


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    reserved: Optional[int] = None
    location: Optional[str] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    is_active: Optional[bool] = None


class InventoryResponse(InventoryBase):
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InventoryTransactionBase(BaseModel):
    inventory_id: Optional[str] = None
    product_id: str
    change: int
    reason: Optional[str] = None
    reference: Optional[str] = None


class InventoryTransactionCreate(InventoryTransactionBase):
    pass


class InventoryTransactionResponse(InventoryTransactionBase):
    id: uuid.UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
