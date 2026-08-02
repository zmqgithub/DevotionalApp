# app/api/v1/endpoints/cities.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.cities.service import CityService
from app.modules.cities.schemas import CityCreate, CityUpdate, CityResponse
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CityResponse])
async def get_cities(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        state_id: Optional[int] = None,
        search: Optional[str] = None,
        is_capital: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all cities"""
    service = CityService(db)

    if state_id:
        cities = service.get_by_state(state_id)
        total = len(cities)
    elif search:
        cities = service.search_cities(search)
        total = len(cities)
    elif is_capital is not None:
        cities = service.get_capital_cities()
        total = len(cities)
    else:
        cities = service.get_all(skip=skip, limit=limit)
        total = service.count()

    return PaginatedResponse(
        items=cities,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    """Get city by ID"""
    service = CityService(db)
    return service.get_by_id(city_id)


@router.post("/", response_model=CityResponse)
async def create_city(
        city_data: CityCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new city (admin only)"""
    service = CityService(db)
    return service.create(city_data)


@router.put("/{city_id}", response_model=CityResponse)
async def update_city(
        city_id: int,
        city_data: CityUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a city (admin only)"""
    service = CityService(db)
    return service.update(city_id, city_data)


@router.delete("/{city_id}")
async def delete_city(
        city_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a city (super admin only)"""
    service = CityService(db)
    service.delete(city_id)
    return MessageResponse(message="City deleted successfully")