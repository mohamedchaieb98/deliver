from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.crud import client as crud_client
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter()
# avec Depends : FastAPI se charge d'ouvrir la session au début de la requête et de la fermer 
# automatiquement dès que la réponse est envoyée au client, même si une erreur survient pendant l'exécution.
@router.get("/", response_model=List[ClientResponse])
def get_clients(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des clients actifs"""
    return crud_client.get_active_clients(db, skip=skip, limit=limit)

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_in: ClientCreate, 
    db: Session = Depends(get_db)
):
    """Créer un nouveau client"""
    return crud_client.create_client(db=db, client_data=client_in.dict())

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: UUID, 
    db: Session = Depends(get_db)
):
    """Récupérer un client spécifique par son ID"""
    client = crud_client.get_client_by_id(db, client_id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client( 
    client_id: UUID,  
    client_in: ClientUpdate, 
    db: Session = Depends(get_db)
):
    """Mettre à jour les infos d'un client"""
    # exclude_unset=True pour ne mettre à jour que les champs envoyés
    client = crud_client.update_client(db, client_id=client_id, update_data=client_in.dict(exclude_unset=True))
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.delete("/{client_id}", response_model=dict)
def delete_client(
    client_id: UUID, 
    db: Session = Depends(get_db)
):
    """Supprimer (désactiver) un client"""
    client = crud_client.delete_client(db, client_id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return {"message": "Client désactivé avec succès"}