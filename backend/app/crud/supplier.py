from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.models.products import Supplier
import uuid

# Create : ajout d'un frs
def create_supplier(db: Session, supplier_data: dict):
    supplier_data=Supplier(**supplier_data)
    db.add(supplier_data)
    db.commit()
    db.refresh(supplier_data)
    return supplier_data

# Read : récupérer un frs par son ID
def get_supplier_by_id(db: Session, supplier_id: str):
    return db.query(Supplier).filter(Supplier.id == str(supplier_id), Supplier.is_active == True).first()

# Read : récupérer tous les frs actifs
def get_active_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Supplier).filter(Supplier.is_active == True).offset(skip).limit(limit).all()

# Update : mettre à jour les infos d'un frs
def update_supplier(db: Session, supplier_id: str, update_data: dict):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        return None
    for key, value in update_data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier

# Delete : désactiver un frs
def delete_supplier(db: Session, supplier_id: str):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        return None
    supplier.is_active = False
    db.commit()
    return supplier

