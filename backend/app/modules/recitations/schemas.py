from __future__ import annotations
from pydantic import Field
from typing import Optional, Any
from app.schemas.base import BaseSchema, TimestampSchema

class RecitationBase(BaseSchema):
    title: str = Field(..., max_length=255)
    audio_url: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=500)
    duration: Optional[float] = None
    transcript: Optional[str] = None
    translation: Optional[str] = None
    order: int = 0
    extra_data: Optional[Any] = None

class RecitationCreate(RecitationBase):
    content_id: int
    language_id: Optional[int] = None

class RecitationUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=255)
    audio_url: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=500)
    duration: Optional[float] = None
    transcript: Optional[str] = None
    translation: Optional[str] = None
    is_published: Optional[bool] = None
    order: Optional[int] = None
    extra_data: Optional[Any] = None

class RecitationResponse(RecitationBase, TimestampSchema):
    id: int
    content_id: int
    language_id: Optional[int] = None
    is_published: bool
    language_name: Optional[str] = None