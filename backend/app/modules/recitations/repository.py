from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.recitations.model import Recitation
from app.modules.recitations.schemas import RecitationCreate, RecitationUpdate


class RecitationRepository(BaseRepository[Recitation, RecitationCreate, RecitationUpdate]):
    """Repository for Recitation model"""

    def __init__(self, db: Session):
        super().__init__(db, Recitation)

    def get_by_content(self, content_id: int) -> List[Recitation]:
        """Get all recitations for a content item"""
        return self.db.query(Recitation).filter(
            Recitation.content_id == content_id
        ).order_by(Recitation.order).all()

    def get_published_recitations(self) -> List[Recitation]:
        """Get all published recitations"""
        return self.db.query(Recitation).filter(
            Recitation.is_published == True
        ).all()

    def get_by_language(self, language_id: int) -> List[Recitation]:
        """Get recitations by language"""
        return self.db.query(Recitation).filter(
            Recitation.language_id == language_id,
            Recitation.is_published == True
        ).all()