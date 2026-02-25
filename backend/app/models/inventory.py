from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Inventory(Base):
    """Stock courant par produit (par emplacement si besoin)."""
    __tablename__ = "inventories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    reserved = Column(Integer, nullable=False, default=0)
    location = Column(String(200), nullable=True)
    min_stock = Column(Integer, nullable=True)
    max_stock = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relation vers le produit
    product = relationship("Product", back_populates="inventory_items")


class InventoryTransaction(Base):
    """Historique des mouvements de stock pour audit et recalculs."""
    __tablename__ = "inventory_transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    inventory_id = Column(String(36), ForeignKey("inventories.id"), nullable=True, index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    change = Column(Integer, nullable=False)  # positif = entrée, négatif = sortie
    reason = Column(String(500), nullable=True)
    reference = Column(String(200), nullable=True)  # ex: order id, supplier order, adjustment
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    inventory = relationship("Inventory")
    product = relationship("Product")
