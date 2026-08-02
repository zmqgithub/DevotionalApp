from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.announcements.repository import AnnouncementRepository
from app.modules.announcements.model import Announcement
from app.modules.announcements.schemas import AnnouncementCreate, AnnouncementUpdate
from app.core.exceptions import ValidationError


class AnnouncementService(BaseService[Announcement, AnnouncementCreate, AnnouncementUpdate]):
    """Service for Announcement business logic"""

    def __init__(self, db: Session):
        self.repository = AnnouncementRepository(db)
        super().__init__(self.repository)

    def get_active_announcements(self) -> List[Announcement]:
        """Get all active announcements"""
        return self.repository.get_active_announcements()

    def get_featured_announcements(self) -> List[Announcement]:
        """Get featured announcements"""
        return self.repository.get_featured_announcements()

    def get_announcements_for_user(self, user_id: int) -> List[Announcement]:
        """Get announcements targeted for a specific user"""
        return self.repository.get_announcements_for_user(user_id)

    def publish_now(self, announcement_id: int) -> Announcement:
        """Publish an announcement immediately"""
        announcement = self.get_by_id(announcement_id)
        if announcement.is_active:
            raise ValidationError("Announcement is already active")

        now = datetime.utcnow()
        announcement.is_active = True
        announcement.show_from = now

        return self.repository.update(announcement_id, announcement)

    def schedule_announcement(self, announcement_id: int, show_from: datetime,
                              show_until: Optional[datetime] = None) -> Announcement:
        """Schedule an announcement"""
        announcement = self.get_by_id(announcement_id)

        if show_from < datetime.utcnow():
            raise ValidationError("Show from date cannot be in the past")

        if show_until and show_until <= show_from:
            raise ValidationError("Show until date must be after show from date")

        announcement.show_from = show_from
        announcement.show_until = show_until

        return self.repository.update(announcement_id, announcement)

    def _validate_create(self, obj_in: AnnouncementCreate) -> None:
        """Validate announcement creation"""
        if obj_in.show_from and obj_in.show_from < datetime.utcnow():
            raise ValidationError("Show from date cannot be in the past")

        if obj_in.show_from and obj_in.show_until and obj_in.show_until <= obj_in.show_from:
            raise ValidationError("Show until date must be after show from date")