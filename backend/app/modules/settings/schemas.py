from __future__ import annotations
from pydantic import Field
from typing import Optional, Dict, Any
from app.schemas.base import BaseSchema, TimestampSchema

class SettingsBase(BaseSchema):
    theme: str = Field(default="light", pattern="^(light|dark|system)$")
    language: str = Field(default="en", max_length=10)
    timezone: str = Field(default="UTC", max_length=50)
    notifications_enabled: bool = True
    email_notifications: bool = True
    push_notifications: bool = True
    two_factor_enabled: bool = False
    privacy_settings: Dict[str, Any] = {}
    display_settings: Dict[str, Any] = {}

class SettingsCreate(SettingsBase):
    user_id: int

class SettingsUpdate(BaseSchema):
    theme: Optional[str] = Field(None, pattern="^(light|dark|system)$")
    language: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None
    privacy_settings: Optional[Dict[str, Any]] = None
    display_settings: Optional[Dict[str, Any]] = None

class SettingsResponse(SettingsBase, TimestampSchema):
    id: int
    user_id: int