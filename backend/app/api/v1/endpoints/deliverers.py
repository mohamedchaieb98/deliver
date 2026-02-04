from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.deliverer import Deliverer
from app.schemas.deliverer import DelivererCreate, DelivererUpdate, DelivererResponse

router = APIRouter()

@router.get("/", response_model=List[DelivererResponse])
def get_deliverers(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    territory: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all deliverers with optional filters"""
    query = db.query(Deliverer)
    
    # Apply filters
    if active is not None:
        query = query.filter(Deliverer.is_available == active)
    if territory:
        query = query.filter(Deliverer.territory == territory)
    
    deliverers = query.offset(skip).limit(limit).all()
    return deliverers

@router.post("/", response_model=DelivererResponse)
def create_deliverer(
    deliverer: DelivererCreate,
    db: Session = Depends(get_db)
):
    """Create a new deliverer"""
    # Check if employee_id already exists
    existing = db.query(Deliverer).filter(Deliverer.employee_id == deliverer.employee_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Deliverer with employee_id '{deliverer.employee_id}' already exists"
        )
    
    # Create new deliverer
    db_deliverer = Deliverer(**deliverer.dict())
    db.add(db_deliverer)
    db.commit()
    db.refresh(db_deliverer)
    return db_deliverer

@router.get("/{deliverer_id}", response_model=DelivererResponse)
def get_deliverer(deliverer_id: str, db: Session = Depends(get_db)):
    """Get a specific deliverer by ID"""
    deliverer = db.query(Deliverer).filter(Deliverer.id == deliverer_id).first()
    if not deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverer not found"
        )
    return deliverer

@router.put("/{deliverer_id}", response_model=DelivererResponse)
def update_deliverer(
    deliverer_id: str,
    deliverer: DelivererUpdate,
    db: Session = Depends(get_db)
):
    """Update a deliverer"""
    db_deliverer = db.query(Deliverer).filter(Deliverer.id == deliverer_id).first()
    if not db_deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverer not found"
        )
    
    # Update fields
    update_data = deliverer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_deliverer, field, value)
    
    db.commit()
    db.refresh(db_deliverer)
    return db_deliverer

@router.delete("/{deliverer_id}")
def delete_deliverer(deliverer_id: str, db: Session = Depends(get_db)):
    """Delete a deliverer"""
    db_deliverer = db.query(Deliverer).filter(Deliverer.id == deliverer_id).first()
    if not db_deliverer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverer not found"
        )
    
    db.delete(db_deliverer)
    db.commit()
    return {"message": "Deliverer deleted successfully"}

@router.get("/stats/summary")
def get_deliverer_stats(db: Session = Depends(get_db)):
    """Get deliverer statistics"""
    total = db.query(Deliverer).count()
    available = db.query(Deliverer).filter(Deliverer.is_available == True).count()
    
    return {
        "total_deliverers": total,
        "available_deliverers": available,
        "unavailable_deliverers": total - available
    }