from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.models.products import Product
import uuid

# Create : ajout d'un produit
def create_product(db:Session , product_data : dict):
    product_data= Product(**product_data)  # Transforme le dictionnaire en objet Product
    db.add(product_data)
    db.commit()
    db.refresh(product_data)  # Recharge l'objet pour avoir l'ID généré
    return product_data

# READ : Lire un produit par son ID
def get_product_by_id(db:Session, product_id:str):
    return db.query(Product).filter(Product.id == str(product_id)).first()

# READ ALL : Liste des produits
def get_all_products(db:Session):
    return db.query(Product).all()

# UPDATE : Mettre à jour un produit
def update_product(db: Session, product_id: str, update_data: dict):
    product_obj = db.query(Product).filter(Product.id == str(product_id)).first()
    
    if product_obj:
        for key, value in update_data.items():
            setattr(product_obj, key, value)
        db.commit()
        db.refresh(product_obj)
    return product_obj

# DELETE (soft delete) : Supprimer un produit (cad désactiver au lieu de supprimer directement)
def delete_product(db: Session, product_id: str):
    product = db.query(Product).filter(Product.id == str(product_id)).first()
    if product:
        product.is_active = False  # Désactiver le produit au lieu de le supprimer
        db.commit()  # Sauvegarder les changements
        db.refresh(product)  # Recharger l'objet pour avoir les données à jour
    return product
