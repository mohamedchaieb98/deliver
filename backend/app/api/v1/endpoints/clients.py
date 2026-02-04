from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_clients():
    """Get all clients"""
    return [{"message": "Clients endpoint working"}]

@router.post("/")
def create_client():
    """Create a new client"""
    return {"message": "Create client endpoint"}

@router.get("/{client_id}")
def get_client(client_id: str):
    """Get client by ID"""
    return {"message": f"Client {client_id}"}

@router.put("/{client_id}")
def update_client(client_id: str):
    """Update client"""
    return {"message": f"Updated client {client_id}"}

@router.delete("/{client_id}")
def delete_client(client_id: str):
    """Delete client"""
    return {"message": "Client deleted successfully"}