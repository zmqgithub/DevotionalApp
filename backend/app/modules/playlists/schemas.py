from __future__ import annotations

from datetime import datetime

from pydantic import Field
from typing import Optional, List, Any
from app.schemas.base import BaseSchema, TimestampSchema

class PlaylistBase(BaseSchema):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    is_public: bool = True

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None

class PlaylistResponse(PlaylistBase, TimestampSchema):
    id: int
    user_id: int
    is_active: bool
    item_count: int = 0

# Use forward reference for PlaylistItemResponse
class PlaylistDetailResponse(PlaylistResponse):
    items: Optional[List['PlaylistItemResponse']] = []

# Define the referenced class after usage
class PlaylistItemResponse(BaseSchema):
    id: int
    playlist_id: int
    content_id: int
    order: int
    notes: Optional[Any] = None
    created_at: Optional[datetime] = None
    content_title: Optional[str] = None
    content_type: Optional[str] = None
    content_duration: Optional[int] = None

# Rebuild to resolve forward references
PlaylistDetailResponse.model_rebuild()