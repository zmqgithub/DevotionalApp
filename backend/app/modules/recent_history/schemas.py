from __future__ import annotations
from pydantic import Field
from typing import Optional, Any
from app.schemas.base import BaseSchema, TimestampSchema

class RecentHistoryBase(BaseSchema):
    progress: float = Field(default=0, ge=0, le=100)
    last_position: Optional[int] = None
    extra_data: Optional[Any] = None

class RecentHistoryCreate(RecentHistoryBase):
    content_id: int

class RecentHistoryUpdate(BaseSchema):
    progress: Optional[float] = Field(None, ge=0, le=100)
    last_position: Optional[int] = None
    extra_data: Optional[Any] = None

class RecentHistoryResponse(RecentHistoryBase, TimestampSchema):
    id: int
    user_id: int
    content_id: int
    content_title: Optional[str] = None
    content_type: Optional[str] = None
    content_featured_image: Optional[str] = None