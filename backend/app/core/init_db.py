"""
Database initialization and setup utilities
"""
from sqlalchemy import inspect

from app.core.database import Base, SessionLocal, engine
from app.models.client import Client
from app.models.deliverer import Deliverer
from app.models.products import Product, Supplier
from app.models.sales import Order, Reseller


def check_tables_exist():
    """Check if all required tables exist in the database"""
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        required_tables = [
            "deliverers",
            "clients",
            "resellers",
            "orders",
            "payments",
            "products",
            "suppliers",
            "supplier_products",
            "supplier_orders",
            "order_items",
            "inventories",
            "inventory_transactions",
            "routes",
            "expenses",
        ]

        missing_tables = [
            table for table in required_tables if table not in existing_tables
        ]

        if missing_tables:
            print(f"[INFO] Missing tables: {missing_tables}")
            return False
        else:
            print(f"[INFO] All {len(required_tables)} tables exist")
            return True

    except Exception as e:
        print(f"[ERROR] Failed to check tables: {e}")
        return False


def create_tables():
    """Create all database tables"""
    try:
        print("[INFO] Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("[INFO] Database tables created successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create tables: {e}")
        return False


def init_database():
    """Initialize database - check tables and create if needed"""
    print("[INFO] Initializing database...")

    # Check if tables exist
    if check_tables_exist():
        print("[INFO] Database is ready!")
        return True

    # Create tables if they don't exist
    print("[INFO] Setting up database for first time...")
    if create_tables():
        # Verify tables were created
        if check_tables_exist():
            print("[INFO] Database initialization completed successfully!")
            return True
        else:
            print("[ERROR] Tables creation verification failed!")
            return False
    else:
        print("[ERROR] Database initialization failed!")
        return False


def get_database_stats():
    """Get basic statistics about the database"""
    try:
        db = SessionLocal()
        stats = {
            "deliverers": db.query(Deliverer).count(),
            "clients": db.query(Client).count(),
            "resellers": db.query(Reseller).count(),
            "orders": db.query(Order).count(),
            "products": db.query(Product).count(),
            "suppliers": db.query(Supplier).count(),
        }
        db.close()
        return stats
    except Exception as e:
        print(f"[ERROR] Failed to get database stats: {e}")
        return None


def seed_sample_data():
    """Add some sample data if database is empty"""
    try:
        db = SessionLocal()

        # Check if we already have data
        if db.query(Deliverer).count() > 0:
            print("[INFO] Sample data already exists")
            db.close()
            return True

        print("[INFO] Adding sample data...")

        # Add sample deliverers
        sample_deliverers = [
            Deliverer(
                name="Ahmed Hassan",
                employee_id="EMP001",
                email="ahmed@waterdelivery.com",
                phone_number="+212612345678",
                territory="Downtown",
                is_available=True,
            ),
            Deliverer(
                name="Fatima Zahra",
                employee_id="EMP002",
                email="fatima@waterdelivery.com",
                phone_number="+212612345679",
                territory="Uptown",
                is_available=True,
            ),
        ]

        for deliverer in sample_deliverers:
            db.add(deliverer)

        # Add sample client
        sample_client = Client(
            name="Test Restaurant",
            business_name="Cafe Central",
            email="cafe@central.com",
            phone_number="+212612345680",
            address="123 Main Street, City Center",
            client_type="business",
            payment_terms="net30",
        )
        db.add(sample_client)

        db.commit()
        print("[INFO] Sample data added successfully!")
        db.close()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to seed sample data: {e}")
        if "db" in locals():
            db.rollback()
            db.close()
        return False
