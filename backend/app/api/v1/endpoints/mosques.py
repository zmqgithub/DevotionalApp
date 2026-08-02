from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.mosques.service import MosqueService
from app.modules.mosques.schemas import MosqueCreate, MosqueUpdate, MosqueResponse
from app.api.v1.dependencies import get_current_user, get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[MosqueResponse])
async def get_mosques(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        city_id: Optional[int] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = True,
        is_verified: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all mosques"""
    service = MosqueService(db)

    if city_id:
        mosques = service.get_by_city(city_id)
        total = len(mosques)
    elif search:
        mosques = service.search_mosques(search)
        total = len(mosques)
    else:
        filters = {}
        if is_active is not None:
            filters['is_active'] = is_active
        if is_verified is not None:
            filters['is_verified'] = is_verified
        mosques = service.get_all(skip=skip, limit=limit, filters=filters)
        total = service.count(filters)

    return PaginatedResponse(
        items=mosques,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/nearby", response_model=List[MosqueResponse])
async def get_nearby_mosques(
        latitude: float = Query(..., ge=-90, le=90),
        longitude: float = Query(..., ge=-180, le=180),
        radius_km: float = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    """Get mosques near a location"""
    service = MosqueService(db)
    return service.get_by_location(latitude, longitude, radius_km)


@router.get("/verified", response_model=List[MosqueResponse])
async def get_verified_mosques(
        db: Session = Depends(get_db)
):
    """Get all verified mosques"""
    service = MosqueService(db)
    return service.get_verified_mosques()


@router.get("/{mosque_id}", response_model=MosqueResponse)
async def get_mosque(
        mosque_id: int,
        db: Session = Depends(get_db)
):
    """Get mosque by ID"""
    service = MosqueService(db)
    return service.get_by_id(mosque_id)


@router.post("/", response_model=MosqueResponse)
async def create_mosque(
        mosque_data: MosqueCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new mosque (admin only)"""
    service = MosqueService(db)
    return service.create(mosque_data)


@router.put("/{mosque_id}", response_model=MosqueResponse)
async def update_mosque(
        mosque_id: int,
        mosque_data: MosqueUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a mosque (admin only)"""
    service = MosqueService(db)
    return service.update(mosque_id, mosque_data)


@router.post("/{mosque_id}/verify", response_model=MosqueResponse)
async def verify_mosque(
        mosque_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Verify a mosque (super admin only)"""
    service = MosqueService(db)
    return service.verify_mosque(mosque_id)


@router.delete("/{mosque_id}")
async def delete_mosque(
        mosque_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a mosque (super admin only)"""
    service = MosqueService(db)
    service.delete(mosque_id)
    return MessageResponse(message="Mosque deleted successfully")