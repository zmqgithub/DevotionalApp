from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.repositories.base import BaseRepository
from app.modules.ratings.model import Rating
from app.modules.ratings.schemas import RatingCreate, RatingUpdate


class RatingRepository(BaseRepository[Rating, RatingCreate, RatingUpdate]):
    """Repository for Rating model"""

    def __init__(self, db: Session):
        super().__init__(db, Rating)

    def get_by_content(self, content_id: int) -> List[Rating]:
        """Get all ratings for a content item"""
        return self.db.query(Rating).filter(
            Rating.content_id == content_id
        ).order_by(Rating.created_at.desc()).all()

    def get_by_user_and_content(self, user_id: int, content_id: int) -> Optional[Rating]:
        """Get a user's rating for content"""
        return self.db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.content_id == content_id
        ).first()

    def get_content_rating_stats(self, content_id: int) -> dict:
        """Get rating statistics for content"""
        stats = self.db.query(
            func.avg(Rating.rating).label('average'),
            func.count(Rating.id).label('total'),
            func.sum(func.case((Rating.rating == 5, 1), else_=0)).label('five_stars'),
            func.sum(func.case((Rating.rating == 4, 1), else_=0)).label('four_stars'),
            func.sum(func.case((Rating.rating == 3, 1), else_=0)).label('three_stars'),
            func.sum(func.case((Rating.rating == 2, 1), else_=0)).label('two_stars'),
            func.sum(func.case((Rating.rating == 1, 1), else_=0)).label('one_star')
        ).filter(Rating.content_id == content_id).first()

        if not stats.total:
            return {
                'average': 0,
                'total': 0,
                'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }

        return {
            'average': float(stats.average or 0),
            'total': stats.total,
            'distribution': {
                1: stats.one_star or 0,
                2: stats.two_stars or 0,
                3: stats.three_stars or 0,
                4: stats.four_stars or 0,
                5: stats.five_stars or 0
            }
        }