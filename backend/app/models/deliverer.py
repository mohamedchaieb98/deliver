from sqlalchemy import Column, String, Boolean, Date, DateTime, Text, JSON
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Deliverer(Base):
    __tablename__ = "deliverers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(200), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    vehicle_info = Column(JSON, nullable=True)  # JSON works with SQLite
    license_number = Column(String(50), nullable=True)
    phone_number = Column(String(20), nullable=True)
    hire_date = Column(Date, nullable=True)
    territory = Column(String(100), nullable=True, index=True)
    is_available = Column(Boolean, default=True, index=True)
    current_location = Column(String(100), nullable=True)
    last_location_update = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())