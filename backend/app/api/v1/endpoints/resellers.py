from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import resseller as crud_reseller
from app.schemas.reseller import ResellerCreate, ResellerResponse, ResellerUpdate

router = APIRouter()


@router.get("/", response_model=List[ResellerResponse])
def get_resellers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer la liste des resellers actifs"""
    return crud_reseller.get_active_resellers(db, skip=skip, limit=limit)


@router.post("/", response_model=ResellerResponse, status_code=status.HTTP_201_CREATED)
def create_reseller(reseller_in: ResellerCreate, db: Session = Depends(get_db)):
    """Créer un nouveau reseller"""
    return crud_reseller.create_reseller(db=db, reseller_data=reseller_in.dict())


@router.get("/{reseller_id}", response_model=ResellerResponse)
def get_reseller(reseller_id: UUID, db: Session = Depends(get_db)):
    """Récupérer un reseller spécifique par son ID"""
    reseller = crud_reseller.get_reseller_by_id(db, reseller_id=reseller_id)
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller non trouvé")
    return reseller


@router.put("/{reseller_id}", response_model=ResellerResponse)
def update_reseller(
    reseller_id: UUID, reseller_in: ResellerUpdate, db: Session = Depends(get_db)
):
    """Mettre à jour les infos d'un reseller"""
    # exclude_unset=True pour ne mettre à jour que les champs envoyés
    reseller = crud_reseller.update_reseller(
        db, reseller_id=reseller_id, update_data=reseller_in.dict(exclude_unset=True)
    )
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller non trouvé")
    return reseller


@router.delete("/{reseller_id}", response_model=dict)
def delete_reseller(reseller_id: UUID, db: Session = Depends(get_db)):
    """Supprimer (désactiver) un reseller"""
    reseller = crud_reseller.delete_reseller(db, reseller_id=reseller_id)
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller non trouvé")
    return {"message": "Reseller désactivé avec succès"}


@router.get("/{reseller_id}/orders")
def get_reseller_orders(reseller_id: UUID, db: Session = Depends(get_db)):
    """Récupérer les commandes d'un reseller"""
    reseller = crud_reseller.get_reseller_by_id(db, reseller_id=reseller_id)
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller non trouvé")

    # Pour l'instant, retourner une liste vide
    # TODO: Implémenter la logique pour récupérer les commandes
    return {"reseller_id": str(reseller_id), "orders": []}


@router.get("/stats/summary")
def get_reseller_stats(db: Session = Depends(get_db)):
    """Récupérer les statistiques des resellers"""
    from app.models.sales import Reseller

    total = db.query(Reseller).count()
    active = db.query(Reseller).filter(Reseller.is_active == True).count()

    return {
        "total_resellers": total,
        "active_resellers": active,
        "inactive_resellers": total - active,
    }
