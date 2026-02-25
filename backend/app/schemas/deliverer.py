import uuid
from datetime import date, datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

# Front ➔ Back	React dit : "Crée-moi ce livreur avec ces infos".


class DelivererBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    employee_id: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    vehicle_info: Optional[Dict[str, Any]] = None
    license_number: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    hire_date: Optional[date] = None
    territory: Optional[str] = Field(None, max_length=100)
    is_available: bool = True


class DelivererCreate(DelivererBase):
    pass


# Front ➔ Back	React dit : "Modifie seulement ces 2 champs là".


class DelivererUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    vehicle_info: Optional[Dict[str, Any]] = None
    license_number: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    territory: Optional[str] = Field(None, max_length=100)
    is_available: Optional[bool] = None


# Back ➔ Front	Le Back dit : "Voici les données complètes (avec ID et dates) à afficher".


class DelivererResponse(DelivererBase):
    id: uuid.UUID
    current_location: Optional[str] = None
    last_location_update: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
