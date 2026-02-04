"""
Database setup script
Run this to create the database tables
"""
from app.core.database import Base, engine
from app.models.deliverer import Deliverer
# Import other models as we create them

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()