# tout ce qui concerne la vente

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Reseller(Base):
    __tablename__ = "resellers"
    
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    business_name = Column(String(200), nullable=False)
    contact_person = Column(String(200), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # Relation : Un revendeur peut avoir plusieurs commandes
    orders = relationship("Order", back_populates="reseller")

class Order(Base):
    __tablename__ = "orders"
    
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    order_number = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    #CLÉ ÉTRANGÈRE : La commande appartient à un revendeur
    # reseller_id = Column(UUID(as_uuid=True), ForeignKey("resellers.id"))
    reseller_id = Column(String(36), ForeignKey("resellers.id"), nullable=False, index=True)
    reseller = relationship("Reseller", back_populates="orders")


class Payment(Base):
    __tablename__ = "payments"
    
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    payment_method = Column(String(20), nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())