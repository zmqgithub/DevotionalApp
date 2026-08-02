from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.announcements.service import AnnouncementService
from app.modules.announcements.schemas import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from app.api.v1.dependencies import get_current_user, get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[AnnouncementResponse])
async def get_announcements(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        is_active: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Get all announcements (admin only)"""
    service = AnnouncementService(db)

    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active
    if is_featured is not None:
        filters['is_featured'] = is_featured

    announcements = service.get_all(skip=skip, limit=limit, filters=filters)
    total = service.count(filters)

    return PaginatedResponse(
        items=announcements,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/active", response_model=List[AnnouncementResponse])
async def get_active_announcements(
        db: Session = Depends(get_db)
):
    """Get all active announcements"""
    service = AnnouncementService(db)
    return service.get_active_announcements()


@router.get("/featured", response_model=List[AnnouncementResponse])
async def get_featured_announcements(
        db: Session = Depends(get_db)
):
    """Get featured announcements"""
    service = AnnouncementService(db)
    return service.get_featured_announcements()


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
        announcement_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Get announcement by ID (admin only)"""
    service = AnnouncementService(db)
    return service.get_by_id(announcement_id)


@router.post("/", response_model=AnnouncementResponse)
async def create_announcement(
        announcement_data: AnnouncementCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new announcement (admin only)"""
    service = AnnouncementService(db)
    return service.create(announcement_data)


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
        announcement_id: int,
        announcement_data: AnnouncementUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update an announcement (admin only)"""
    service = AnnouncementService(db)
    return service.update(announcement_id, announcement_data)


@router.post("/{announcement_id}/publish")
async def publish_announcement(
        announcement_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Publish an announcement (admin only)"""
    service = AnnouncementService(db)
    service.publish_now(announcement_id)
    return MessageResponse(message="Announcement published successfully")


@router.delete("/{announcement_id}")
async def delete_announcement(
        announcement_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete an announcement (super admin only)"""
    service = AnnouncementService(db)
    service.delete(announcement_id)
    return MessageResponse(message="Announcement deleted successfully")