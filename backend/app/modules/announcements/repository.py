from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.repositories.base import BaseRepository
from app.modules.announcements.model import Announcement
from app.modules.announcements.schemas import AnnouncementCreate, AnnouncementUpdate


class AnnouncementRepository(BaseRepository[Announcement, AnnouncementCreate, AnnouncementUpdate]):
    """Repository for Announcement model"""

    def __init__(self, db: Session):
        super().__init__(db, Announcement)

    def get_active_announcements(self) -> List[Announcement]:
        """Get all active announcements"""
        now = datetime.utcnow()
        return self.db.query(Announcement).filter(
            Announcement.is_active == True,
            or_(
                Announcement.show_from.is_(None),
                Announcement.show_from <= now
            ),
            or_(
                Announcement.show_until.is_(None),
                Announcement.show_until >= now
            )
        ).order_by(Announcement.priority.desc()).all()

    def get_featured_announcements(self) -> List[Announcement]:
        """Get featured announcements"""
        return self.get_active_announcements().filter(
            Announcement.is_featured == True
        ).all()

    def get_announcements_for_user(self, user_id: int) -> List[Announcement]:
        """Get announcements targeted for a specific user"""
        announcements = self.get_active_announcements()
        # This would be more complex with actual targeting logic
        return announcements