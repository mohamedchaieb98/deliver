from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.models.sales import Order
import uuid

# Create : ajout d'une commande
def create_order(db: Session, order_data: dict):
    order_data = Order(**order_data)  # Transforme le dictionnaire en objet Order
    db.add(order_data)
    db.commit()
    db.refresh(order_data)  # Recharge l'objet pour avoir l'ID généré
    return order_data

# READ : Lire une commande par son ID
def get_order_by_id(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == str(order_id)).first()

# READ ALL : Liste des commandes
def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

# UPDATE : Mettre à jour une commande
def update_order(db: Session, order_id: str, update_data: dict):
    order_obj = db.query(Order).filter(Order.id == str(order_id)).first()
    
    if order_obj:
        for key, value in update_data.items():
            setattr(order_obj, key, value)
        db.commit()
        db.refresh(order_obj)
    return order_obj

# DELETE : Supprimer une commande
def delete_order(db: Session, order_id: str):
    order = db.query(Order).filter(Order.id == str(order_id)).first()
    if order:
        db.delete(order)
        db.commit()
        return True
    return False

