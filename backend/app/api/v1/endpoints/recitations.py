from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.recitations.service import RecitationService
from app.modules.recitations.schemas import RecitationCreate, RecitationUpdate, RecitationResponse
from app.api.v1.dependencies import get_current_user, get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[RecitationResponse])
async def get_recitations(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        content_id: Optional[int] = None,
        language_id: Optional[int] = None,
        is_published: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all recitations"""
    service = RecitationService(db)

    if content_id:
        recitations = service.get_by_content(content_id)
        total = len(recitations)
    elif language_id:
        recitations = service.get_by_language(language_id)
        total = len(recitations)
    else:
        filters = {}
        if is_published is not None:
            filters['is_published'] = is_published
        recitations = service.get_all(skip=skip, limit=limit, filters=filters)
        total = service.count(filters)

    return PaginatedResponse(
        items=recitations,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{recitation_id}", response_model=RecitationResponse)
async def get_recitation(
        recitation_id: int,
        db: Session = Depends(get_db)
):
    """Get recitation by ID"""
    service = RecitationService(db)
    return service.get_by_id(recitation_id)


@router.post("/", response_model=RecitationResponse)
async def create_recitation(
        recitation_data: RecitationCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new recitation (admin only)"""
    service = RecitationService(db)
    return service.create(recitation_data)


@router.put("/{recitation_id}", response_model=RecitationResponse)
async def update_recitation(
        recitation_id: int,
        recitation_data: RecitationUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a recitation (admin only)"""
    service = RecitationService(db)
    return service.update(recitation_id, recitation_data)


@router.post("/{recitation_id}/publish", response_model=RecitationResponse)
async def publish_recitation(
        recitation_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Publish a recitation (admin only)"""
    service = RecitationService(db)
    return service.publish_recitation(recitation_id)


@router.post("/{recitation_id}/unpublish", response_model=RecitationResponse)
async def unpublish_recitation(
        recitation_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Unpublish a recitation (admin only)"""
    service = RecitationService(db)
    return service.unpublish_recitation(recitation_id)


@router.post("/content/{content_id}/reorder")
async def reorder_recitations(
        content_id: int,
        recitation_ids: List[int],
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Reorder recitations for a content (admin only)"""
    service = RecitationService(db)
    service.reorder_recitations(content_id, recitation_ids)
    return MessageResponse(message="Recitations reordered successfully")


@router.delete("/{recitation_id}")
async def delete_recitation(
        recitation_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a recitation (super admin only)"""
    service = RecitationService(db)
    service.delete(recitation_id)
    return MessageResponse(message="Recitation deleted successfully")