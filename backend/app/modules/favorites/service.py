from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.favorites.repository import FavoriteRepository
from app.modules.favorites.model import Favorite
from app.modules.favorites.schemas import FavoriteCreate
from app.core.exceptions import DuplicateError


class FavoriteService(BaseService[Favorite, FavoriteCreate, FavoriteCreate]):
    """Service for Favorite business logic"""

    def __init__(self, db: Session):
        self.repository = FavoriteRepository(db)
        super().__init__(self.repository)

    def get_by_user(self, user_id: int) -> List[Favorite]:
        """Get all favorites for a user"""
        return self.repository.get_by_user(user_id)

    def get_by_user_and_content(self, user_id: int, content_id: int) -> Optional[Favorite]:
        """Get a specific favorite"""
        return self.repository.get_by_user_and_content(user_id, content_id)

    def is_favorited(self, user_id: int, content_id: int) -> bool:
        """Check if a content is favorited by a user"""
        return self.repository.is_favorited(user_id, content_id)

    def toggle_favorite(self, user_id: int, content_id: int) -> dict:
        """Toggle favorite status"""
        existing = self.get_by_user_and_content(user_id, content_id)

        if existing:
            # Remove from favorites
            self.repository.delete(existing.id)
            return {"is_favorited": False, "message": "Removed from favorites"}
        else:
            # Add to favorites
            favorite_data = FavoriteCreate(content_id=content_id)
            self.create(favorite_data)
            return {"is_favorited": True, "message": "Added to favorites"}

    def get_favorite_content_ids(self, user_id: int) -> List[int]:
        """Get all content IDs favorited by a user"""
        return self.repository.get_favorite_content_ids(user_id)

    def _check_duplicate_on_create(self, obj_in: FavoriteCreate) -> None:
        """Check for duplicate favorite"""
        if self.repository.get_by_user_and_content(obj_in.user_id, obj_in.content_id):
            raise DuplicateError("Content is already in favorites")