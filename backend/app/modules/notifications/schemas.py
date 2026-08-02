from __future__ import annotations
from pydantic import Field
from typing import Optional, Any
from datetime import datetime
from enum import Enum
from app.schemas.base import BaseSchema

class NotificationType(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class NotificationBase(BaseSchema):
    title: str = Field(..., max_length=255)
    message: str
    type: NotificationType = NotificationType.INFO
    priority: NotificationPriority = NotificationPriority.MEDIUM
    extra_data: Optional[Any] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseSchema):
    is_read: Optional[bool] = None
    is_deleted: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    is_deleted: bool
    created_at: datetime
    read_at: Optional[datetime] = None