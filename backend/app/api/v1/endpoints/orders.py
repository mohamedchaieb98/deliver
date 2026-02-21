from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.crud import order as crud_order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)):
    orders = crud_order.get_all_orders(db, skip=skip, limit=limit)
    return orders

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db, order.dict())

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: UUID, order_update: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = crud_order.update_order(db, order_id=order_id, update_data=order_update.dict(exclude_unset=True))
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order

@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: str, db: Session = Depends(get_db)):
    deleted = crud_order.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"message": "Order deleted successfully"}