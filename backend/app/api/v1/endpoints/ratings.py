from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.ratings.service import RatingService
from app.modules.ratings.schemas import RatingCreate, RatingUpdate, RatingResponse
from app.api.v1.dependencies import get_current_user
from app.modules.users.model import User
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("/content/{content_id}", response_model=List[RatingResponse])
async def get_content_ratings(
        content_id: int,
        db: Session = Depends(get_db)
):
    """Get all ratings for a content"""
    service = RatingService(db)
    return service.get_by_content(content_id)


@router.get("/content/{content_id}/stats")
async def get_content_rating_stats(
        content_id: int,
        db: Session = Depends(get_db)
):
    """Get rating statistics for content"""
    service = RatingService(db)
    return service.get_content_rating_stats(content_id)


@router.post("/", response_model=RatingResponse)
async def rate_content(
        rating_data: RatingCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Rate a content"""
    service = RatingService(db)
    return service.rate_content(
        user_id=current_user.id,
        content_id=rating_data.content_id,
        rating=rating_data.rating,
        review=rating_data.review
    )


@router.get("/me/{content_id}")
async def get_my_rating(
        content_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get current user's rating for a content"""
    service = RatingService(db)
    rating = service.get_by_user_and_content(current_user.id, content_id)
    if not rating:
        return {"rating": None}
    return rating


@router.delete("/{rating_id}")
async def delete_rating(
        rating_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete a rating"""
    service = RatingService(db)
    rating = service.get_by_id(rating_id)

    if rating.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this rating"
        )

    service.delete(rating_id)
    return MessageResponse(message="Rating deleted successfully")