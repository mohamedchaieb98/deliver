import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

# front -> back


class ClientBase(BaseModel):
    # On utilise exactement les mêmes noms que dans models.py
    name: str
    business_name: Optional[str] = None
    email: Optional[EmailStr] = None  # EmailStr valide le format de l'email
    phone_number: Optional[str] = None
    address: str
    client_type: Optional[str] = "individual"
    payment_terms: Optional[str] = "cash"


class ClientCreate(ClientBase):
    # Pas besoin de rajouter 'nom' ou 'prenom' ici !
    # Ils sont déjà inclus via ClientBase.
    pass  # On utilise les champs de base pour créer


# front -> back


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    business_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    client_type: Optional[str] = None
    payment_terms: Optional[str] = None
    is_active: Optional[bool] = None


# back -> front


class ClientResponse(ClientBase):
    # Ici, on utilise str ou uuid.UUID (Pydantic gère la conversion)
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
