from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Supplier(Base):
    """Modèle pour les fournisseurs"""
    __tablename__ = "suppliers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(200), nullable=False, index=True)
    contact_person = Column(String(200), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations (using string references to avoid circular imports)
    supplier_orders = relationship("SupplierOrder", back_populates="supplier", foreign_keys="SupplierOrder.supplier_id")
    supplier_products = relationship("SupplierProduct", back_populates="supplier", foreign_keys="SupplierProduct.supplier_id")


class Product(Base):
    """Modèle pour les produits"""
    __tablename__ = "products"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    category = Column(String(50), nullable=False, index=True)
    size = Column(String(20), nullable=True)
    sku = Column(String(50), unique=True, nullable=False) #Stock Keeping Unit
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    order_items = relationship("OrderItem", back_populates="product")
    supplier_products = relationship("SupplierProduct", back_populates="product")
    inventory_items = relationship("Inventory", back_populates="product")


class SupplierProduct(Base):
    """Table de liaison : Produits disponibles chez les fournisseurs"""
    __tablename__ = "supplier_products"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    supplier_sku = Column(String(100), nullable=True)
    unit_price = Column(Numeric(10, 2), nullable=False)
    min_quantity = Column(Integer, default=1)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    supplier = relationship("Supplier", back_populates="supplier_products")
    product = relationship("Product", back_populates="supplier_products")


class SupplierOrder(Base):
    """Modèle pour les commandes auprès des fournisseurs"""
    __tablename__ = "supplier_orders"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"), nullable=False, index=True)
    status = Column(String(20), default='pending')
    total_amount = Column(Numeric(12, 2), default=0)
    expected_delivery = Column(DateTime(timezone=True), nullable=True)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    supplier = relationship("Supplier", back_populates="supplier_orders")
    order_items = relationship("OrderItem", back_populates="supplier_order", cascade="all, delete-orphan")


class OrderItem(Base):
    """Modèle pour les articles de commande fournisseur"""
    __tablename__ = "order_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    supplier_order_id = Column(String(36), ForeignKey("supplier_orders.id"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    supplier_order = relationship("SupplierOrder", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")