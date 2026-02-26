# tout ce qui concerne la vente

import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Reseller(Base):
    __tablename__ = "resellers"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    business_name = Column(String(200), nullable=False)
    contact_person = Column(String(200), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # Relation : Un revendeur peut avoir plusieurs commandes
    orders = relationship("Order", back_populates="reseller")


class Order(Base):
    __tablename__ = "orders"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    order_number = Column(String(20), unique=True, nullable=False)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=True, index=True)
    reseller_id = Column(
        String(36), ForeignKey("resellers.id"), nullable=True, index=True
    )
    deliverer_id = Column(
        String(36), ForeignKey("deliverers.id"), nullable=True, index=True
    )
    status = Column(String(20), default="pending")
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    delivery_address = Column(String(500), nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relations
    reseller = relationship("Reseller", back_populates="orders")
    items = relationship(
        "CustomerOrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class Payment(Base):
    __tablename__ = "payments"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False, default=0)
    payment_method = Column(String(20), nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    transaction_id = Column(String(100), nullable=True, index=True)
    status = Column(String(20), default="pending", index=True)
    processed_by = Column(String(36), nullable=True)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CustomerOrderItem(Base):
    """Model for customer order items"""

    __tablename__ = "customer_order_items"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    order = relationship("Order", back_populates="items")
