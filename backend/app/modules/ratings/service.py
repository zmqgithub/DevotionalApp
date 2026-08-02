from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.ratings.repository import RatingRepository
from app.modules.ratings.model import Rating
from app.modules.ratings.schemas import RatingCreate, RatingUpdate
from app.core.exceptions import ValidationError


class RatingService(BaseService[Rating, RatingCreate, RatingUpdate]):
    """Service for Rating business logic"""

    def __init__(self, db: Session):
        self.repository = RatingRepository(db)
        super().__init__(self.repository)

    def get_by_content(self, content_id: int) -> List[Rating]:
        """Get all ratings for a content item"""
        return self.repository.get_by_content(content_id)

    def get_by_user_and_content(self, user_id: int, content_id: int) -> Optional[Rating]:
        """Get a user's rating for content"""
        return self.repository.get_by_user_and_content(user_id, content_id)

    def rate_content(self, user_id: int, content_id: int, rating: int, review: Optional[str] = None) -> Rating:
        """Rate a content item"""
        # Check if content allows ratings
        from app.modules.contents.service import ContentService
        content_service = ContentService(self.repository.db)
        content = content_service.get_by_id(content_id)

        if not content.allow_rating:
            raise ValidationError("Ratings are disabled for this content")

        # Check if user already rated this content
        existing = self.get_by_user_and_content(user_id, content_id)

        if existing:
            # Update existing rating
            update_data = {"rating": rating}
            if review is not None:
                update_data["review"] = review
            return self.update(existing.id, update_data)
        else:
            # Create new rating
            rating_data = RatingCreate(
                rating=rating,
                review=review,
                content_id=content_id,
                user_id=user_id
            )
            return self.create(rating_data)

    def get_content_rating_stats(self, content_id: int) -> Dict[str, Any]:
        """Get rating statistics for content"""
        return self.repository.get_content_rating_stats(content_id)

    def get_average_rating(self, content_id: int) -> float:
        """Get average rating for content"""
        stats = self.get_content_rating_stats(content_id)
        return stats['average']

    def _validate_create(self, obj_in: RatingCreate) -> None:
        """Validate rating creation"""
        if not 1 <= obj_in.rating <= 5:
            raise ValidationError("Rating must be between 1 and 5")