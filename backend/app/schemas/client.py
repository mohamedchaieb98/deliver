from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class ClientBase(BaseModel):
    name: str
    business_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class ClientResponse(ClientBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True