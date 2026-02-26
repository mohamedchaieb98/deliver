import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sales import CustomerOrderItem, Order


# Create : ajout d'une commande
def create_order(db: Session, order_data: dict):
    # Extract items from order_data
    items_data = order_data.pop("items", [])

    # Convert string dates to datetime objects if needed
    if "order_date" in order_data and order_data["order_date"]:
        if isinstance(order_data["order_date"], str):
            try:
                order_data["order_date"] = datetime.fromisoformat(
                    order_data["order_date"].replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                order_data["order_date"] = datetime.now()
    else:
        order_data["order_date"] = datetime.now()

    if "delivery_date" in order_data and order_data["delivery_date"]:
        if isinstance(order_data["delivery_date"], str):
            try:
                order_data["delivery_date"] = datetime.fromisoformat(
                    order_data["delivery_date"].replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                order_data["delivery_date"] = None

    # Set default values
    if "id" not in order_data:
        order_data["id"] = str(uuid.uuid4())
    if "created_at" not in order_data:
        order_data["created_at"] = datetime.now()
    if "updated_at" not in order_data:
        order_data["updated_at"] = datetime.now()

    # Create the order
    order_obj = Order(**order_data)
    db.add(order_obj)
    db.commit()
    db.refresh(order_obj)

    # Create order items
    for item_data in items_data:
        item_obj = CustomerOrderItem(
            id=str(uuid.uuid4()),
            order_id=order_obj.id,
            created_at=datetime.now(),
            **item_data,
        )
        db.add(item_obj)

    db.commit()
    db.refresh(order_obj)
    return order_obj


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
        # Handle items separately
        items_data = update_data.pop("items", None)

        # Update order fields
        for key, value in update_data.items():
            setattr(order_obj, key, value)

        # Update items if provided
        if items_data is not None:
            # Delete existing items
            db.query(CustomerOrderItem).filter(
                CustomerOrderItem.order_id == str(order_id)
            ).delete()

            # Create new items
            for item_data in items_data:
                item_obj = CustomerOrderItem(order_id=order_obj.id, **item_data)
                db.add(item_obj)

        db.commit()
        db.refresh(order_obj)
    return order_obj


def delete_order(db: Session, order_id: str):
    try:
        order = db.query(Order).filter(Order.id == str(order_id)).first()
        if order:
            from app.models.sales import Payment

            payments = db.query(Payment).filter(Payment.order_id == str(order_id)).all()
            for payment in payments:
                db.delete(payment)

            # Delete order items (cascade should handle this, but let's be explicit)
            db.query(CustomerOrderItem).filter(
                CustomerOrderItem.order_id == str(order_id)
            ).delete()

            db.delete(order)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting order: {e}")
        return False
