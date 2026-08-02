from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.modules.notifications.service import NotificationService
from app.modules.notifications.schemas import NotificationCreate, NotificationResponse
from app.api.v1.dependencies import get_current_user, get_current_superuser
from app.modules.users.model import User
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
async def get_my_notifications(
        unread_only: bool = False,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get current user's notifications"""
    service = NotificationService(db)
    return service.get_by_user(current_user.id, unread_only)


@router.get("/unread-count")
async def get_unread_count(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get unread notification count"""
    service = NotificationService(db)
    count = service.get_unread_count(current_user.id)
    return {"unread_count": count}


@router.post("/{notification_id}/read")
async def mark_as_read(
        notification_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    service = NotificationService(db)
    service.mark_as_read(notification_id)
    return MessageResponse(message="Notification marked as read")


@router.post("/read-all")
async def mark_all_as_read(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Mark all notifications as read"""
    service = NotificationService(db)
    service.mark_all_as_read(current_user.id)
    return MessageResponse(message="All notifications marked as read")


@router.delete("/{notification_id}")
async def delete_notification(
        notification_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete a notification"""
    service = NotificationService(db)
    notification = service.get_by_id(notification_id)

    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this notification"
        )

    service.delete(notification_id)
    return MessageResponse(message="Notification deleted successfully")


@router.post("/send", response_model=NotificationResponse)
async def send_notification(
        notification_data: NotificationCreate,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Send notification to a user (admin only)"""
    service = NotificationService(db)
    return service.create(notification_data)