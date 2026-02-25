from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import supplier as crud_supplier
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate

router = APIRouter()


@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_supplier.get_active_suppliers(db, skip=skip, limit=limit)


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier_update: SupplierCreate, db: Session = Depends(get_db)):
    return crud_supplier.create_supplier(db=db, supplier_data=supplier_update.dict())


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    supplier = crud_supplier.get_supplier_by_id(db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: UUID, supplier_update: SupplierUpdate, db: Session = Depends(get_db)
):
    supplier = crud_supplier.update_supplier(
        db,
        supplier_id=supplier_id,
        update_data=supplier_update.dict(exclude_unset=True),
    )
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.delete("/{supplier_id}", response_model=SupplierResponse)
def delete_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    supplier = crud_supplier.delete_supplier(db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier
