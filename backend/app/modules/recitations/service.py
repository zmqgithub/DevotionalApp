from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.recitations.repository import RecitationRepository
from app.modules.recitations.model import Recitation
from app.modules.recitations.schemas import RecitationCreate, RecitationUpdate
from app.core.exceptions import ValidationError, NotFoundError


class RecitationService(BaseService[Recitation, RecitationCreate, RecitationUpdate]):
    """Service for Recitation business logic"""

    def __init__(self, db: Session):
        self.repository = RecitationRepository(db)
        super().__init__(self.repository)

    def get_by_content(self, content_id: int) -> List[Recitation]:
        """Get all recitations for a content item"""
        return self.repository.get_by_content(content_id)

    def get_published_recitations(self) -> List[Recitation]:
        """Get all published recitations"""
        return self.repository.get_published_recitations()

    def get_by_language(self, language_id: int) -> List[Recitation]:
        """Get recitations by language"""
        return self.repository.get_by_language(language_id)

    def publish_recitation(self, recitation_id: int) -> Recitation:
        """Publish a recitation"""
        recitation = self.get_by_id(recitation_id)
        if recitation.is_published:
            raise ValidationError("Recitation is already published")

        recitation.is_published = True
        return self.repository.update(recitation_id, recitation)

    def unpublish_recitation(self, recitation_id: int) -> Recitation:
        """Unpublish a recitation"""
        recitation = self.get_by_id(recitation_id)
        if not recitation.is_published:
            raise ValidationError("Recitation is not published")

        recitation.is_published = False
        return self.repository.update(recitation_id, recitation)

    def reorder_recitations(self, content_id: int, recitation_ids: List[int]) -> bool:
        """Reorder recitations for a content item"""
        # Verify all recitations belong to this content
        for recitation_id in recitation_ids:
            recitation = self.repository.get_by_id(recitation_id)
            if not recitation or recitation.content_id != content_id:
                raise ValidationError(f"Recitation with ID {recitation_id} does not belong to this content")

        # Update order
        for index, recitation_id in enumerate(recitation_ids):
            self.repository.update(recitation_id, {"order": index})

        return True

    def _validate_create(self, obj_in: RecitationCreate) -> None:
        """Validate recitation creation"""
        # At least one of audio_url or video_url must be provided
        if not obj_in.audio_url and not obj_in.video_url:
            raise ValidationError("At least one of audio_url or video_url is required")

        if obj_in.duration and obj_in.duration <= 0:
            raise ValidationError("Duration must be greater than 0")