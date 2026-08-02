from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class DedicationBase(BaseSchema):
    name: str = Field(..., max_length=255)
    message: Optional[str] = Field(None, max_length=1000)
    is_public: bool = True
    is_anonymous: bool = False

class DedicationCreate(DedicationBase):
    content_id: int

class DedicationUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = Field(None, max_length=1000)
    is_public: Optional[bool] = None
    is_anonymous: Optional[bool] = None

class DedicationResponse(DedicationBase, TimestampSchema):
    id: int
    user_id: int
    content_id: int
    content_title: Optional[str] = None