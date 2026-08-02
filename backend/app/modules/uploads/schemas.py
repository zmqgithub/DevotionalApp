from __future__ import annotations
from pydantic import Field
from typing import Optional, Any
from datetime import datetime
from enum import Enum
from app.schemas.base import BaseSchema

class UploadType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

class UploadBase(BaseSchema):
    file_name: str = Field(..., max_length=255)
    file_url: str = Field(..., max_length=500)
    file_path: str = Field(..., max_length=500)
    file_size: int
    mime_type: str = Field(..., max_length=100)
    upload_type: UploadType
    is_public: bool = True
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None
    extra_data: Optional[Any] = None

class UploadCreate(UploadBase):
    user_id: int

class UploadUpdate(BaseSchema):
    is_public: Optional[bool] = None
    extra_data: Optional[Any] = None

class UploadResponse(UploadBase):
    id: int
    user_id: int
    is_processed: bool
    created_at: datetime
    updated_at: datetime