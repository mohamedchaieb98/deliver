from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_products():
    return []

@router.post("/")
def create_product():
    return {}

@router.get("/{product_id}")
def get_product(product_id: str):
    return {}

@router.put("/{product_id}")
def update_product(product_id: str):
    return {}

@router.delete("/{product_id}")
def delete_product(product_id: str):
    return {"message": "Product deleted successfully"}