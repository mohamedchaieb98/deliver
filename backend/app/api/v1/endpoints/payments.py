from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import payment as crud_payment
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter()


@router.get("/", response_model=List[PaymentResponse])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_payment.get_all_payments(db, skip=skip, limit=limit)


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment_in: PaymentCreate, db: Session = Depends(get_db)):
    return crud_payment.create_payment(db=db, payment_data=payment_in.dict())


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = crud_payment.get_payment_by_id(db, payment_id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: str, payment_in: PaymentUpdate, db: Session = Depends(get_db)
):
    payment = crud_payment.update_payment(
        db, payment_id=payment_id, update_data=payment_in.dict(exclude_unset=True)
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.delete("/{payment_id}", response_model=dict)
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    deleted = crud_payment.delete_payment(db, payment_id=payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}
