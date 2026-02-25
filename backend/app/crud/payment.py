import uuid

from sqlalchemy.orm import Session

from app.models.sales import Payment


# Create : ajout d'un paiement
def create_payment(db: Session, payment_data: dict):
    # convert UUID values to string for SQLite compatibility
    for k, v in list(payment_data.items()):
        if isinstance(v, uuid.UUID):
            payment_data[k] = str(v)

    payment_obj = Payment(**payment_data)
    db.add(payment_obj)
    db.commit()
    db.refresh(payment_obj)
    return payment_obj


# READ : Lire un paiement par son ID
def get_payment_by_id(db: Session, payment_id: str):
    return db.query(Payment).filter(Payment.id == str(payment_id)).first()


# READ ALL : Liste des paiements
def get_all_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()


# UPDATE : Mettre à jour un paiement
def update_payment(db: Session, payment_id: str, update_data: dict):
    payment_obj = db.query(Payment).filter(Payment.id == str(payment_id)).first()
    if payment_obj:
        for key, value in update_data.items():
            if isinstance(value, uuid.UUID):
                value = str(value)
            setattr(payment_obj, key, value)
        db.commit()
        db.refresh(payment_obj)
    return payment_obj


# DELETE : Supprimer un paiement
def delete_payment(db: Session, payment_id: str):
    payment = db.query(Payment).filter(Payment.id == str(payment_id)).first()
    if payment:
        db.delete(payment)
        db.commit()
        return True
    return False
