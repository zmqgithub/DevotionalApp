from __future__ import annotations
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema

class FavoriteCreate(BaseSchema):
    content_id: int

class FavoriteResponse(BaseSchema):
    id: int
    user_id: int
    content_id: int
    created_at: datetime
    content_title: Optional[str] = None
    content_type: Optional[str] = None
    content_featured_image: Optional[str] = None