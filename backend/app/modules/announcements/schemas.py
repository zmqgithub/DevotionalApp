from __future__ import annotations
from pydantic import Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampSchema

class AnnouncementBase(BaseSchema):
    title: str = Field(..., max_length=255)
    content: str
    is_active: bool = True
    is_featured: bool = False
    priority: int = Field(default=0, ge=0, le=10)
    target_audience: Optional[Dict[str, Any]] = None
    show_from: Optional[datetime] = None
    show_until: Optional[datetime] = None
    image_url: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    extra_data: Optional[Dict[str, Any]] = None

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=0, le=10)
    target_audience: Optional[Dict[str, Any]] = None
    show_from: Optional[datetime] = None
    show_until: Optional[datetime] = None
    image_url: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    extra_data: Optional[Dict[str, Any]] = None

class AnnouncementResponse(AnnouncementBase, TimestampSchema):
    id: int
    created_by: int