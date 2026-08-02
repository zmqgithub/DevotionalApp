from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class PermissionBase(BaseSchema):
    name: str = Field(..., min_length=3, max_length=100)
    resource: str = Field(..., min_length=3, max_length=100)
    action: str = Field(..., min_length=3, max_length=50)  # create, read, update, delete, manage
    description: Optional[str] = Field(None, max_length=500)

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    resource: Optional[str] = Field(None, min_length=3, max_length=100)
    action: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class PermissionResponse(PermissionBase, TimestampSchema):
    id: int
    is_active: bool