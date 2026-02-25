from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric, Date, Time, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Route(Base):
    __tablename__ = "routes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    route_name = Column(String(100), nullable=True, index=True)
    deliverer_id = Column(String(36), ForeignKey("deliverers.id"), nullable=True, index=True)
    route_date = Column(Date, nullable=True, index=True)
    status = Column(String(20), default='planned', index=True)
    planned_start_time = Column(Time, nullable=True)
    actual_start_time = Column(Time, nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # minutes
    actual_duration = Column(Integer, nullable=True)     # minutes
    total_distance = Column(Numeric(8, 2), nullable=True) # kilometers
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    # deliverer_id = Column(String(36), ForeignKey("deliverers.id"), nullable=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False, default=0) #Montant de la dépense
    description = Column(String(1000), nullable=False)
    expense_date = Column(Date, nullable=False)
    receipt_photo_path = Column(String(500), nullable=True)
    location = Column(String(200), nullable=True)
    is_reimbursable = Column(Boolean, default=True)
    status = Column(String(20), default='pending')
    approved_by = Column(String(36), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())