from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Force SQLite for development
DATABASE_URL = "sqlite:///./water_delivery.db"

# SQLite Database (for development)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# No Redis for now
redis_client = None
print("✅ Using SQLite database for development")

# Database dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis dependency for FastAPI
def get_redis():
    return redis_client