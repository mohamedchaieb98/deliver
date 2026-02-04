from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_suppliers():
    return []

@router.post("/")
def create_supplier():
    return {}

@router.get("/{supplier_id}")
def get_supplier(supplier_id: str):
    return {}

@router.put("/{supplier_id}")
def update_supplier(supplier_id: str):
    return {}

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: str):
    return {"message": "Supplier deleted successfully"}