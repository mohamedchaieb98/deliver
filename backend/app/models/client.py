import uuid

from sqlalchemy import Boolean, Column, DateTime, Numeric, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    # VERSION COMPATIBLE : On utilise String pour SQLite, mais le type peut être casté en UUID plus tard
    # 'default' avec uuid.uuid4 sans les parenthèses pour que SQLAlchemy l'exécute à chaque création
    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )

    name = Column(String(200), nullable=False, index=True)
    business_name = Column(String(200), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(Text, nullable=False)

    # Utilisation de Numeric au lieu de DECIMAL pour une meilleure compatibilité entre SQLite et Postgres
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)

    client_type = Column(String(20), default="individual")
    payment_terms = Column(String(20), default="cash")

    credit_limit = Column(Numeric(10, 2), default=0)
    outstanding_balance = Column(Numeric(10, 2), default=0)

    is_active = Column(Boolean, default=True, index=True)
    notes = Column(Text, nullable=True)

    # func.now() fonctionne sur les deux systèmes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
