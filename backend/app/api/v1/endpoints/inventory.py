from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import inventory as crud_inventory
from app.models.inventory import Inventory as InventoryModel
from app.schemas.inventory import InventoryCreate, InventoryResponse, InventoryUpdate

router = APIRouter()


@router.get("/low-stock", response_model=List[InventoryResponse])
def get_low_stock(db: Session = Depends(get_db)):
    """Récupérer les inventaires sous le seuil minimum"""
    # Récupérer tous les inventaires actifs avec un min_stock défini
    inventories = (
        db.query(InventoryModel)
        .filter(
            InventoryModel.is_active == True,
            InventoryModel.min_stock.is_not(None),
            InventoryModel.quantity < InventoryModel.min_stock,
        )
        .all()
    )
    return inventories


# CRUD - Inventaire
@router.get("/", response_model=List[InventoryResponse])
def get_inventories(db: Session = Depends(get_db)):
    """Récupérer la liste des inventaires"""
    return crud_inventory.get_all_inventories(db)


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(inventory_in: InventoryCreate, db: Session = Depends(get_db)):
    """Créer un nouvel inventaire"""
    return crud_inventory.create_inventory(db=db, inventory_data=inventory_in.dict())


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(inventory_id: str, db: Session = Depends(get_db)):
    """Récupérer un inventaire spécifique par son ID"""
    inventory = crud_inventory.get_inventory_by_id(db, inventory_id=inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventaire non trouvé")
    return inventory


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: str, inventory_in: InventoryUpdate, db: Session = Depends(get_db)
):
    """Mettre à jour les infos d'un inventaire"""
    inventory = crud_inventory.update_inventory(
        db, inventory_id=inventory_id, update_data=inventory_in.dict(exclude_unset=True)
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventaire non trouvé")
    return inventory


@router.delete("/{inventory_id}", response_model=dict)
def delete_inventory(inventory_id: str, db: Session = Depends(get_db)):
    """Supprimer (désactiver) un inventaire"""
    inventory = crud_inventory.delete_inventory(db, inventory_id=inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventaire non trouvé")
    return {"message": "Inventaire désactivé avec succès"}


# Endpoints spécialisés
@router.get("/product/{product_id}", response_model=List[InventoryResponse])
def get_inventories_by_product(product_id: str, db: Session = Depends(get_db)):
    """Récupérer les inventaires pour un produit spécifique"""
    inventories = crud_inventory.get_inventories_by_product(db, product_id=product_id)
    if not inventories:
        raise HTTPException(
            status_code=404, detail="Aucun inventaire trouvé pour ce produit"
        )
    return inventories
