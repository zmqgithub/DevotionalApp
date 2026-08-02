from __future__ import annotations
from pydantic import Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.schemas.base import BaseSchema

class AuditLogBase(BaseSchema):
    action: str = Field(..., max_length=100)
    resource_type: str = Field(..., max_length=100)
    resource_id: Optional[int] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = Field(None, max_length=500)
    extra_data: Optional[Dict[str, Any]] = None

class AuditLogCreate(AuditLogBase):
    user_id: Optional[int] = None

class AuditLogResponse(AuditLogBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    username: Optional[str] = None