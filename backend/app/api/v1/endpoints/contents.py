from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.contents.service import ContentService
from app.modules.contents.schemas import (
    ContentCreate, ContentUpdate, ContentResponse,
    ContentDetailResponse, ContentType, ContentStatus
)
from app.api.v1.dependencies import get_current_user, get_current_superuser
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ContentResponse])
async def get_contents(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        content_type: Optional[ContentType] = None,
        category_id: Optional[int] = None,
        is_featured: Optional[bool] = None,
        is_premium: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all published contents with filters"""
    service = ContentService(db)
    filters = {}
    if content_type:
        filters['content_type'] = content_type
    if category_id:
        filters['category_id'] = category_id
    if is_featured is not None:
        filters['is_featured'] = is_featured
    if is_premium is not None:
        filters['is_premium'] = is_premium

    contents = service.get_published_content(
        skip=skip,
        limit=limit,
        filters=filters
    )
    total = service.count(filters)

    return PaginatedResponse(
        items=contents,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/featured", response_model=List[ContentResponse])
async def get_featured_contents(
        limit: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db)
):
    """Get featured contents"""
    service = ContentService(db)
    return service.get_featured_content(limit)


@router.get("/trending", response_model=List[ContentResponse])
async def get_trending_contents(
        limit: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db)
):
    """Get trending contents"""
    service = ContentService(db)
    return service.get_trending_content(limit)


@router.get("/search", response_model=List[ContentResponse])
async def search_contents(
        q: str = Query(..., min_length=2),
        content_type: Optional[ContentType] = None,
        category_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """Search contents"""
    service = ContentService(db)
    return service.search_content(q, content_type, category_id)


@router.get("/{content_id}", response_model=ContentDetailResponse)
async def get_content(
        content_id: int,
        db: Session = Depends(get_db)
):
    """Get content by ID with all details"""
    service = ContentService(db)
    content = service.get_content_with_relations(content_id)

    # Increment view count
    service.increment_view_count(content_id)

    return content


@router.get("/slug/{slug}", response_model=ContentDetailResponse)
async def get_content_by_slug(
        slug: str,
        db: Session = Depends(get_db)
):
    """Get content by slug"""
    service = ContentService(db)
    content = service.get_by_slug(slug)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Increment view count
    service.increment_view_count(content.id)

    return service.get_content_with_relations(content.id)


@router.post("/", response_model=ContentResponse)
async def create_content(
        content_data: ContentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create new content"""
    service = ContentService(db)
    content_data.created_by = current_user.id
    return service.create(content_data)


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
        content_id: int,
        content_data: ContentUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update content"""
    service = ContentService(db)
    content_data.updated_by = current_user.id
    return service.update(content_id, content_data)


@router.delete("/{content_id}")
async def delete_content(
        content_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete content (admin only)"""
    service = ContentService(db)
    service.delete(content_id)
    return {"message": "Content deleted successfully"}


@router.post("/{content_id}/publish", response_model=ContentResponse)
async def publish_content(
        content_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Publish content (admin only)"""
    service = ContentService(db)
    return service.publish_content(content_id)


@router.post("/{content_id}/unpublish", response_model=ContentResponse)
async def unpublish_content(
        content_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Unpublish content (admin only)"""
    service = ContentService(db)
    return service.unpublish_content(content_id)


@router.post("/{content_id}/like")
async def like_content(
        content_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Like content"""
    service = ContentService(db)
    service.increment_like_count(content_id)
    return {"message": "Content liked successfully"}