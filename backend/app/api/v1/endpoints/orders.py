from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_orders():
    return []

@router.post("/")
def create_order():
    return {}

@router.get("/{order_id}")
def get_order(order_id: str):
    return {}

@router.put("/{order_id}")
def update_order(order_id: str):
    return {}

@router.post("/{order_id}/assign")
def assign_order(order_id: str):
    return {}

@router.delete("/{order_id}")
def delete_order(order_id: str):
    return {"message": "Order deleted successfully"}