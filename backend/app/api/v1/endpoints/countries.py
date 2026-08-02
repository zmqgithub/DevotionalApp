# app/api/v1/endpoints/countries.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.countries.service import CountryService
from app.modules.countries.schemas import CountryCreate, CountryUpdate, CountryResponse
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CountryResponse])
async def get_countries(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        search: Optional[str] = None,
        is_active: Optional[bool] = True,
        db: Session = Depends(get_db)
):
    """Get all countries"""
    service = CountryService(db)

    if search:
        countries = service.search_countries(search)
        total = len(countries)
    else:
        filters = {}
        if is_active is not None:
            filters['is_active'] = is_active
        countries = service.get_all(skip=skip, limit=limit, filters=filters)
        total = service.count(filters)

    return PaginatedResponse(
        items=countries,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{country_id}", response_model=CountryResponse)
async def get_country(
        country_id: int,
        db: Session = Depends(get_db)
):
    """Get country by ID"""
    service = CountryService(db)
    return service.get_by_id(country_id)


@router.get("/iso/{iso_code}", response_model=CountryResponse)
async def get_country_by_iso(
        iso_code: str,
        db: Session = Depends(get_db)
):
    """Get country by ISO code"""
    service = CountryService(db)
    country = service.get_by_iso_code(iso_code)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.post("/", response_model=CountryResponse)
async def create_country(
        country_data: CountryCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new country (admin only)"""
    service = CountryService(db)
    return service.create(country_data)


@router.put("/{country_id}", response_model=CountryResponse)
async def update_country(
        country_id: int,
        country_data: CountryUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a country (admin only)"""
    service = CountryService(db)
    return service.update(country_id, country_data)


@router.delete("/{country_id}")
async def delete_country(
        country_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a country (super admin only)"""
    service = CountryService(db)
    service.delete(country_id)
    return MessageResponse(message="Country deleted successfully")