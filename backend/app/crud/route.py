import uuid

from sqlalchemy.orm import Session

from app.models.logistics import Route


def create_route(db: Session, route_data: dict):
    for k, v in list(route_data.items()):
        if isinstance(v, uuid.UUID):
            route_data[k] = str(v)
    route_obj = Route(**route_data)
    db.add(route_obj)
    db.commit()
    db.refresh(route_obj)
    return route_obj


def get_route_by_id(db: Session, route_id: str):
    return db.query(Route).filter(Route.id == str(route_id)).first()


def get_all_routes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Route).offset(skip).limit(limit).all()


def update_route(db: Session, route_id: str, update_data: dict):
    route_obj = db.query(Route).filter(Route.id == str(route_id)).first()
    if route_obj:
        for key, value in update_data.items():
            if isinstance(value, uuid.UUID):
                value = str(value)
            setattr(route_obj, key, value)
        db.commit()
        db.refresh(route_obj)
    return route_obj


def delete_route(db: Session, route_id: str):
    route = db.query(Route).filter(Route.id == str(route_id)).first()
    if route:
        db.delete(route)
        db.commit()
        return True
    return False
