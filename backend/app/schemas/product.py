from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class ProductBase(BaseModel):
    name : str
    description : Optional[str] = None
    category : str
    size : Optional[str] = None
    sku : str
    is_active : bool = True
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    category : Optional[str] = None
    size : Optional[str] = None
    sku : Optional[str] = None
    is_active : Optional[bool] = None

class ProductResponse(ProductBase):
    id : uuid.UUID

    class Config:
        from_attributes = True