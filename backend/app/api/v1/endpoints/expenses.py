from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import expense as crud_expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate

router = APIRouter()


@router.get("/categories")
def get_expense_categories():
    """Get available expense categories"""
    return {
        "categories": [
            "fuel",
            "maintenance",
            "parking",
            "tolls",
            "food",
            "supplies",
            "other",
        ]
    }


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_expense.get_all_expenses(db, skip=skip, limit=limit)


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db)):
    return crud_expense.create_expense(db=db, expense_data=expense_in.dict())


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: UUID, db: Session = Depends(get_db)):
    expense = crud_expense.get_expense_by_id(db, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: UUID, expense_in: ExpenseUpdate, db: Session = Depends(get_db)
):
    expense = crud_expense.update_expense(
        db, expense_id=expense_id, update_data=expense_in.dict(exclude_unset=True)
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/{expense_id}", response_model=dict)
def delete_expense(expense_id: UUID, db: Session = Depends(get_db)):
    deleted = crud_expense.delete_expense(db, expense_id=expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}
