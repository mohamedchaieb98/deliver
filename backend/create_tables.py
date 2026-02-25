"""
Database setup script
Run this to create the database tables
"""
from app.core.database import Base, engine
from app.models.deliverer import Deliverer
from app.models.client import Client
from app.models.sales import Reseller, Order, Payment
from app.models.products import Product, Supplier, SupplierProduct, SupplierOrder, OrderItem
from app.models.inventory import Inventory
from app.models.logistics import Expense

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()