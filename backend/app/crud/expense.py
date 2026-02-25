import uuid

from sqlalchemy.orm import Session

from app.models.logistics import Expense


# Create : ajout d'une dépense
def create_expense(db: Session, expense_data: dict):
    # convert UUID values to string for SQLite compatibility
    for k, v in list(expense_data.items()):
        if isinstance(v, uuid.UUID):
            expense_data[k] = str(v)

    expense_obj = Expense(**expense_data)
    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


# READ : Lire une dépense par son ID
def get_expense_by_id(db: Session, expense_id: str):
    return db.query(Expense).filter(Expense.id == str(expense_id)).first()


# READ ALL : Liste des dépenses
def get_all_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Expense).offset(skip).limit(limit).all()


# UPDATE : Mettre à jour une dépense
def update_expense(db: Session, expense_id, update_data: dict):
    expense_obj = db.query(Expense).filter(Expense.id == str(expense_id)).first()
    if expense_obj:
        # convert UUID values to string before assigning (SQLite binding doesn't accept UUID objects)
        for key, value in update_data.items():
            if isinstance(value, uuid.UUID):
                value = str(value)
            setattr(expense_obj, key, value)
        db.commit()
        db.refresh(expense_obj)
    return expense_obj


# DELETE : Supprimer une dépense
def delete_expense(db: Session, expense_id: str):
    expense = db.query(Expense).filter(Expense.id == str(expense_id)).first()
    if expense:
        db.delete(expense)
        db.commit()
        return True
    return False
