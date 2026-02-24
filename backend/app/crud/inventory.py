from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.models.inventory import Inventory

# Create : ajout d'un inventaire
def create_inventory(db: Session, inventory_data: dict):
	inv = Inventory(**inventory_data)
	db.add(inv)
	db.commit()
	db.refresh(inv)
	return inv


def get_inventory_by_id(db: Session, inventory_id):
	return db.query(Inventory).filter(Inventory.id == str(inventory_id)).first()


def get_all_inventories(db: Session):
	return db.query(Inventory).all()


def get_inventories_by_product(db: Session, product_id):
	return db.query(Inventory).filter(Inventory.product_id == str(product_id)).all()


def update_inventory(db: Session, inventory_id, update_data: dict):
	inv = db.query(Inventory).filter(Inventory.id == str(inventory_id)).first()
	if not inv:
		return None
	for key, value in update_data.items():
		setattr(inv, key, value)
	db.commit()
	db.refresh(inv)
	return inv


def delete_inventory(db: Session, inventory_id):
	inv = db.query(Inventory).filter(Inventory.id == str(inventory_id)).first()
	if not inv:
		return None
	inv.is_active = False
	db.commit()
	db.refresh(inv)
	return inv
