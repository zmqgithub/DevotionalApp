from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.schedules.service import ScheduleService
from app.modules.schedules.schemas import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ScheduleResponse])
async def get_schedules(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        mosque_id: Optional[int] = None,
        event_id: Optional[int] = None,
        is_recurring: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all schedules"""
    service = ScheduleService(db)

    if mosque_id:
        schedules = service.get_by_mosque(mosque_id)
        total = len(schedules)
    elif event_id:
        schedules = service.get_by_event(event_id)
        total = len(schedules)
    else:
        filters = {}
        if is_recurring is not None:
            filters['is_recurring'] = is_recurring
        schedules = service.get_all(skip=skip, limit=limit, filters=filters)
        total = service.count(filters)

    return PaginatedResponse(
        items=schedules,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/mosque/{mosque_id}/active", response_model=List[ScheduleResponse])
async def get_active_mosque_schedules(
        mosque_id: int,
        db: Session = Depends(get_db)
):
    """Get active schedules for a mosque"""
    service = ScheduleService(db)
    return service.get_active_schedules_for_mosque(mosque_id)


@router.get("/recurring", response_model=List[ScheduleResponse])
async def get_recurring_schedules(
        db: Session = Depends(get_db)
):
    """Get all recurring schedules"""
    service = ScheduleService(db)
    return service.get_recurring_schedules()


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
        schedule_id: int,
        db: Session = Depends(get_db)
):
    """Get schedule by ID"""
    service = ScheduleService(db)
    return service.get_by_id(schedule_id)


@router.post("/", response_model=ScheduleResponse)
async def create_schedule(
        schedule_data: ScheduleCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new schedule (admin only)"""
    service = ScheduleService(db)
    return service.create(schedule_data)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
        schedule_id: int,
        schedule_data: ScheduleUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a schedule (admin only)"""
    service = ScheduleService(db)
    return service.update(schedule_id, schedule_data)


@router.delete("/{schedule_id}")
async def delete_schedule(
        schedule_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a schedule (super admin only)"""
    service = ScheduleService(db)
    service.delete(schedule_id)
    return MessageResponse(message="Schedule deleted successfully")