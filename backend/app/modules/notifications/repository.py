from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.notifications.model import Notification
from app.modules.notifications.schemas import NotificationCreate, NotificationUpdate


class NotificationRepository(BaseRepository[Notification, NotificationCreate, NotificationUpdate]):
    """Repository for Notification model"""

    def __init__(self, db: Session):
        super().__init__(db, Notification)

    def get_by_user(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        """Get all notifications for a user"""
        query = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_deleted == False
        )

        if unread_only:
            query = query.filter(Notification.is_read == False)

        return query.order_by(Notification.created_at.desc()).all()

    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """Mark a notification as read"""
        notification = self.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, user_id: int) -> bool:
        """Mark all notifications as read for a user"""
        self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True, "read_at": datetime.utcnow()})
        self.db.commit()
        return True

    def get_unread_count(self, user_id: int) -> int:
        """Get unread notification count for a user"""
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
            Notification.is_deleted == False
        ).count()

    def create_for_user(self, user_id: int, notification_data: dict) -> Notification:
        """Create a notification for a specific user"""
        notification = Notification(
            user_id=user_id,
            **notification_data
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def create_for_multiple_users(self, user_ids: List[int], notification_data: dict) -> List[Notification]:
        """Create notifications for multiple users"""
        notifications = []
        for user_id in user_ids:
            notification = Notification(
                user_id=user_id,
                **notification_data
            )
            notifications.append(notification)

        self.db.add_all(notifications)
        self.db.commit()

        for notification in notifications:
            self.db.refresh(notification)

        return notifications