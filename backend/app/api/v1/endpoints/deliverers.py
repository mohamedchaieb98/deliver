from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import deliverer as crud_deliverer
from app.models.deliverer import Deliverer
from app.schemas.deliverer import DelivererCreate, DelivererResponse, DelivererUpdate

router = APIRouter()


@router.get("/", response_model=List[DelivererResponse])
def get_deliverers(
    # skip: int = 0,
    # limit: int = 100,
    # active: Optional[bool] = None,
    # territory: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all deliverers with optional filters"""
    return crud_deliverer.get_all_deliverers(db)


@router.post("/", response_model=DelivererResponse, status_code=status.HTTP_201_CREATED)
def create_deliverer(deliverer: DelivererCreate, db: Session = Depends(get_db)):
    """Create a new deliverer"""
    return crud_deliverer.create_deliverer(db=db, deliverer_data=deliverer.dict())


@router.get("/{deliverer_id}", response_model=DelivererResponse)
def get_deliverer(deliverer_id: UUID, db: Session = Depends(get_db)):
    """Get a specific deliverer by ID"""
    deliverer = crud_deliverer.get_deliverer_by_id(db, deliverer_id)
    if not deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Deliverer not found"
        )
    return deliverer


@router.put("/{deliverer_id}", response_model=DelivererResponse)
def update_deliverer(
    deliverer_id: UUID, deliverer: DelivererUpdate, db: Session = Depends(get_db)
):
    """Update a deliverer"""
    update_deliverer = crud_deliverer.update_deliverer(
        db, deliverer_id=deliverer_id, update_data=deliverer.dict(exclude_unset=True)
    )
    if not update_deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Deliverer not found"
        )
    return update_deliverer


@router.delete("/{deliverer_id}")
def delete_deliverer(deliverer_id: UUID, db: Session = Depends(get_db)):
    """Delete a deliverer"""
    deleted_deliverer = crud_deliverer.delete_deliverer(db, deliverer_id=deliverer_id)
    if not deleted_deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Deliverer not found"
        )
    return {"message": "Deliverer deleted successfully"}


@router.get("/stats/summary")
def get_deliverer_stats(db: Session = Depends(get_db)):
    """Get deliverer statistics"""
    total = db.query(Deliverer).count()
    available = db.query(Deliverer).filter(Deliverer.is_available == True).count()

    return {
        "total_deliverers": total,
        "available_deliverers": available,
        "unavailable_deliverers": total - available,
    }
