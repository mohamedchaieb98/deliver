from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
import uuid


class RouteBase(BaseModel):
    route_name: Optional[str] = None
    deliverer_id: Optional[uuid.UUID] = None
    route_date: Optional[date] = None
    status: Optional[str] = "planned"
    planned_start_time: Optional[time] = None
    actual_start_time: Optional[time] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None
    total_distance: Optional[float] = None


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    route_name: Optional[str] = None
    deliverer_id: Optional[uuid.UUID] = None
    route_date: Optional[date] = None
    status: Optional[str] = None
    planned_start_time: Optional[time] = None
    actual_start_time: Optional[time] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None
    total_distance: Optional[float] = None


class RouteResponse(RouteBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
