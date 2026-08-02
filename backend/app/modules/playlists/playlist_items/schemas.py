from pydantic import Field
from typing import Optional, Any
from app.schemas.base import BaseSchema, TimestampSchema

class PlaylistItemBase(BaseSchema):
    order: int = 0
    notes: Optional[Any] = None

class PlaylistItemCreate(PlaylistItemBase):
    playlist_id: int
    content_id: int

class PlaylistItemUpdate(BaseSchema):
    order: Optional[int] = None
    notes: Optional[Any] = None

class PlaylistItemResponse(PlaylistItemBase, TimestampSchema):
    id: int
    playlist_id: int
    content_id: int
    content_title: Optional[str] = None
    content_type: Optional[str] = None
    content_duration: Optional[int] = None