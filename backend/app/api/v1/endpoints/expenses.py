from fastapi import APIRouter
from uuid import UUID

router = APIRouter()

@router.get("/")
def get_expenses():
    return []

@router.post("/")
def create_expense():
    return {}

@router.get("/categories")
def get_expense_categories():
    return []

@router.get("/deliverer/{deliverer_id}")
def get_deliverer_expenses(deliverer_id: UUID):
    return []