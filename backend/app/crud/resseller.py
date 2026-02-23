from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.models.sales import Reseller
import uuid

# Create : ajout d'un reseller
def create_reseller(db: Session, reseller_data: dict):
    reseller_obj = Reseller(**reseller_data)  # Transforme le dictionnaire en objet Reseller
    db.add(reseller_obj)  # Prépare l'insertion
    db.commit()  # Sauvegarde dans la base de données
    db.refresh(reseller_obj)  # Recharge l'objet pour avoir l'ID généré
    return reseller_obj

# READ : Lire un reseller par son ID
def get_reseller_by_id(db: Session, reseller_id):
    return db.query(Reseller).filter(Reseller.id == str(reseller_id)).first()

# READ ALL : Liste de tous les resellers
def get_all_resellers(db: Session):
    return db.query(Reseller).all()

# READ ALL : Liste des resellers actifs avec pagination
def get_active_resellers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reseller).filter(Reseller.is_active == True).offset(skip).limit(limit).all()

# UPDATE : Mettre à jour un reseller
def update_reseller(db: Session, reseller_id, update_data: dict):
    reseller_obj = db.query(Reseller).filter(Reseller.id == str(reseller_id)).first()
    
    if reseller_obj:
        for key, value in update_data.items():
            setattr(reseller_obj, key, value)
        db.commit()
        db.refresh(reseller_obj)
    return reseller_obj

# DELETE (soft delete) : Désactiver un reseller
def delete_reseller(db: Session, reseller_id):
    reseller = db.query(Reseller).filter(Reseller.id == str(reseller_id)).first()
    if reseller:
        reseller.is_active = False  # Désactiver au lieu de supprimer
        db.commit()
        db.refresh(reseller)
    return reseller
    