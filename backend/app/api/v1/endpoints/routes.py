from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.crud import route as crud_route
from app.schemas.route import RouteCreate, RouteUpdate, RouteResponse

router = APIRouter()


@router.get("/", response_model=List[RouteResponse])
def get_routes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_route.get_all_routes(db, skip=skip, limit=limit)


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(route_in: RouteCreate, db: Session = Depends(get_db)):
    return crud_route.create_route(db=db, route_data=route_in.dict())


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(route_id: str, db: Session = Depends(get_db)):
    route = crud_route.get_route_by_id(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(route_id: str, route_in: RouteUpdate, db: Session = Depends(get_db)):
    route = crud_route.update_route(db, route_id=route_id, update_data=route_in.dict(exclude_unset=True))
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.delete("/{route_id}", response_model=dict)
def delete_route(route_id: str, db: Session = Depends(get_db)):
    deleted = crud_route.delete_route(db, route_id=route_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Route not found")
    return {"message": "Route deleted successfully"}


@router.post("/{route_id}/optimize")
def optimize_route(route_id: str):
    # Placeholder for route optimization logic
    return {"message": "Route optimized (placeholder)", "route_id": route_id}


@router.get("/deliverer/{deliverer_id}/today", response_model=List[RouteResponse])
def get_deliverer_route_today(deliverer_id: UUID, db: Session = Depends(get_db)):
    # Simple filter by deliverer and route_date == today
    from datetime import date
    all_routes = crud_route.get_all_routes(db)
    return [r for r in all_routes if r.deliverer_id == str(deliverer_id) and (r.route_date == date.today())]