from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_resellers():
    return [{"message": "Resellers endpoint working"}]

@router.post("/")
def create_reseller():
    return {"message": "Create reseller endpoint"}

@router.get("/{reseller_id}")
def get_reseller(reseller_id: str):
    return {"message": f"Reseller {reseller_id}"}

@router.put("/{reseller_id}")
def update_reseller(reseller_id: str):
    return {"message": f"Updated reseller {reseller_id}"}

@router.delete("/{reseller_id}")
def delete_reseller(reseller_id: str):
    return {"message": "Reseller deleted successfully"}