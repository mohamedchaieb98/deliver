from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_payments():
    return []

@router.post("/")
def create_payment():
    return {}

@router.get("/{payment_id}")
def get_payment(payment_id: str):
    return {}

@router.put("/{payment_id}")
def update_payment(payment_id: str):
    return {}