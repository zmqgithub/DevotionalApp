# app/api/v1/endpoints/states.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.states.service import StateService
from app.modules.states.schemas import StateCreate, StateUpdate, StateResponse
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[StateResponse])
async def get_states(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        country_id: Optional[int] = None,
        search: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Get all states"""
    service = StateService(db)

    if country_id:
        states = service.get_by_country(country_id)
        total = len(states)
    elif search:
        states = service.search_states(search)
        total = len(states)
    else:
        states = service.get_all(skip=skip, limit=limit)
        total = service.count()

    return PaginatedResponse(
        items=states,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{state_id}", response_model=StateResponse)
async def get_state(
        state_id: int,
        db: Session = Depends(get_db)
):
    """Get state by ID"""
    service = StateService(db)
    return service.get_by_id(state_id)


@router.post("/", response_model=StateResponse)
async def create_state(
        state_data: StateCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new state (admin only)"""
    service = StateService(db)
    return service.create(state_data)


@router.put("/{state_id}", response_model=StateResponse)
async def update_state(
        state_id: int,
        state_data: StateUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a state (admin only)"""
    service = StateService(db)
    return service.update(state_id, state_data)


@router.delete("/{state_id}")
async def delete_state(
        state_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a state (super admin only)"""
    service = StateService(db)
    service.delete(state_id)
    return MessageResponse(message="State deleted successfully")