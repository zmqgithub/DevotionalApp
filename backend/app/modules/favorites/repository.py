from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.favorites.model import Favorite
from app.modules.favorites.schemas import FavoriteCreate


class FavoriteRepository(BaseRepository[Favorite, FavoriteCreate, FavoriteCreate]):
    """Repository for Favorite model"""

    def __init__(self, db: Session):
        super().__init__(db, Favorite)

    def get_by_user(self, user_id: int) -> List[Favorite]:
        """Get all favorites for a user"""
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id
        ).order_by(Favorite.created_at.desc()).all()

    def get_by_user_and_content(self, user_id: int, content_id: int) -> Optional[Favorite]:
        """Get a specific favorite"""
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.content_id == content_id
        ).first()

    def is_favorited(self, user_id: int, content_id: int) -> bool:
        """Check if a content is favorited by a user"""
        return self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.content_id == content_id
        ).first() is not None

    def get_favorite_content_ids(self, user_id: int) -> List[int]:
        """Get all content IDs favorited by a user"""
        favorites = self.db.query(Favorite).filter(
            Favorite.user_id == user_id
        ).all()
        return [f.content_id for f in favorites]

    def remove_all_favorites(self, user_id: int) -> bool:
        """Remove all favorites for a user"""
        self.db.query(Favorite).filter(Favorite.user_id == user_id).delete()
        self.db.commit()
        return True