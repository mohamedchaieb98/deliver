"""
Seed the database with sample data
"""
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.deliverer import Deliverer
from datetime import date

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_deliverers():
    """Add sample deliverers"""
    db = SessionLocal()
    
    try:
        # Check if we already have data
        existing = db.query(Deliverer).first()
        if existing:
            print("✅ Sample data already exists")
            return
        
        # Create sample deliverers
        deliverers = [
            Deliverer(
                name="Mike Johnson",
                employee_id="EMP001",
                email="mike.johnson@company.com",
                phone_number="+1234567890",
                vehicle_info={
                    "make": "Ford",
                    "model": "Transit",
                    "year": 2022,
                    "plate_number": "ABC-123",
                    "capacity": "500L"
                },
                license_number="DL123456789",
                hire_date=date(2023, 1, 15),
                territory="Downtown",
                is_available=True
            ),
            Deliverer(
                name="Sarah Wilson",
                employee_id="EMP002",
                email="sarah.wilson@company.com",
                phone_number="+1234567891",
                vehicle_info={
                    "make": "Toyota",
                    "model": "Hiace",
                    "year": 2021,
                    "plate_number": "XYZ-456",
                    "capacity": "400L"
                },
                license_number="DL987654321",
                hire_date=date(2023, 3, 10),
                territory="Suburbs",
                is_available=True
            ),
            Deliverer(
                name="Carlos Rodriguez",
                employee_id="EMP003",
                email="carlos.rodriguez@company.com",
                phone_number="+1234567892",
                vehicle_info={
                    "make": "Nissan",
                    "model": "NV200",
                    "year": 2020,
                    "plate_number": "DEF-789",
                    "capacity": "300L"
                },
                license_number="DL456789123",
                hire_date=date(2023, 2, 20),
                territory="Industrial",
                is_available=False  # Currently busy
            )
        ]
        
        for deliverer in deliverers:
            db.add(deliverer)
        
        db.commit()
        print(f"✅ Created {len(deliverers)} sample deliverers")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding database with sample data...")
    seed_deliverers()
    print("✅ Database seeding completed!")