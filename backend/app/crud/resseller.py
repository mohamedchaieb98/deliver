from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.models.sales import Reseller

# Create : ajout d'un resseller
def create_client(db: Session , client):
    