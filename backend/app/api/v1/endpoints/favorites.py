from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.favorites.service import FavoriteService
from app.modules.favorites.schemas import FavoriteResponse
from app.api.v1.dependencies import get_current_user
from app.modules.users.model import User
from app.schemas.base import MessageResponse

router = APIRouter()

@router.get("/", response_model=List[FavoriteResponse])
async def get_my_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's favorites"""
    service = FavoriteService(db)
    return service.get_by_user(current_user.id)

@router.post("/toggle/{content_id}")
async def toggle_favorite(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle favorite status for a content"""
    service = FavoriteService(db)
    result = service.toggle_favorite(current_user.id, content_id)
    return MessageResponse(message=result["message"], is_favorited=result["is_favorited"])

@router.get("/check/{content_id}")
async def check_favorite(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if content is favorited by current user"""
    service = FavoriteService(db)
    is_favorited = service.is_favorited(current_user.id, content_id)
    return {"is_favorited": is_favorited}