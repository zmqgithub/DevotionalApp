from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.model import Notification
from app.modules.notifications.schemas import NotificationCreate, NotificationUpdate
from app.core.exceptions import NotFoundError, ValidationError


class NotificationService(BaseService[Notification, NotificationCreate, NotificationUpdate]):
    """Service for Notification business logic"""

    def __init__(self, db: Session):
        self.repository = NotificationRepository(db)
        super().__init__(self.repository)

    def get_by_user(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        """Get all notifications for a user"""
        return self.repository.get_by_user(user_id, unread_only)

    def mark_as_read(self, notification_id: int) -> Notification:
        """Mark a notification as read"""
        notification = self.get_by_id(notification_id)
        if notification.is_read:
            return notification

        return self.repository.mark_as_read(notification_id)

    def mark_all_as_read(self, user_id: int) -> bool:
        """Mark all notifications as read for a user"""
        return self.repository.mark_all_as_read(user_id)

    def get_unread_count(self, user_id: int) -> int:
        """Get unread notification count for a user"""
        return self.repository.get_unread_count(user_id)

    def create_for_user(self, user_id: int, title: str, message: str, **kwargs) -> Notification:
        """Create a notification for a user"""
        notification_data = {
            "title": title,
            "message": message,
            **kwargs
        }
        return self.repository.create_for_user(user_id, notification_data)

    def create_for_multiple_users(self, user_ids: List[int], title: str, message: str, **kwargs) -> List[Notification]:
        """Create notifications for multiple users"""
        notification_data = {
            "title": title,
            "message": message,
            **kwargs
        }
        return self.repository.create_for_multiple_users(user_ids, notification_data)

    def _validate_delete(self, id: int) -> None:
        """Validate notification deletion"""
        notification = self.get_by_id(id)
        if notification.is_deleted:
            raise ValidationError("Notification is already deleted")