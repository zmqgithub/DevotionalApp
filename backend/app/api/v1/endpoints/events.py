from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.events.service import EventService
from app.modules.events.schemas import EventCreate, EventUpdate, EventResponse
from app.api.v1.dependencies import get_current_user, get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[EventResponse])
async def get_events(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        mosque_id: Optional[int] = None,
        status: Optional[str] = None,
        upcoming: bool = False,
        featured: bool = False,
        db: Session = Depends(get_db)
):
    """Get all events"""
    service = EventService(db)

    if upcoming:
        events = service.get_upcoming_events()
        total = len(events)
    elif featured:
        events = service.get_featured_events(limit)
        total = len(events)
    elif mosque_id:
        events = service.get_by_mosque(mosque_id)
        total = len(events)
    else:
        filters = {}
        if status:
            filters['status'] = status
        events = service.get_all(skip=skip, limit=limit, filters=filters)
        total = service.count(filters)

    return PaginatedResponse(
        items=events,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/ongoing", response_model=List[EventResponse])
async def get_ongoing_events(
        db: Session = Depends(get_db)
):
    """Get ongoing events"""
    service = EventService(db)
    return service.get_ongoing_events()


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
        event_id: int,
        db: Session = Depends(get_db)
):
    """Get event by ID"""
    service = EventService(db)
    return service.get_by_id(event_id)


@router.post("/", response_model=EventResponse)
async def create_event(
        event_data: EventCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new event (admin only)"""
    service = EventService(db)
    return service.create(event_data)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
        event_id: int,
        event_data: EventUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update an event (admin only)"""
    service = EventService(db)
    return service.update(event_id, event_data)


@router.post("/{event_id}/register")
async def register_for_event(
        event_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Register for an event"""
    service = EventService(db)
    service.register_for_event(event_id)
    return MessageResponse(message="Successfully registered for event")


@router.delete("/{event_id}")
async def delete_event(
        event_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete an event (super admin only)"""
    service = EventService(db)
    service.delete(event_id)
    return MessageResponse(message="Event deleted successfully")