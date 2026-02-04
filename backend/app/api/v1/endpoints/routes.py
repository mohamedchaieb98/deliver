from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_routes():
    return []

@router.post("/")
def create_route():
    return {}

@router.get("/{route_id}")
def get_route(route_id: str):
    return {}

@router.post("/{route_id}/optimize")
def optimize_route(route_id: str):
    return {}

@router.get("/deliverer/{deliverer_id}/today")
def get_deliverer_route_today(deliverer_id: str):
    return {}