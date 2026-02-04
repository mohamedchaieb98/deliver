from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_inventory():
    return []

@router.post("/{product_id}/adjust")
def adjust_inventory(product_id: str):
    return {}

@router.get("/low-stock")
def get_low_stock():
    return []