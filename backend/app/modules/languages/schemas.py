from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class LanguageBase(BaseSchema):
    name: str = Field(..., max_length=100)
    code: str = Field(..., min_length=2, max_length=10)
    native_name: Optional[str] = Field(None, max_length=100)
    direction: str = Field(default="ltr", pattern="^(ltr|rtl)$")

class LanguageCreate(LanguageBase):
    country_id: Optional[int] = None

class LanguageUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, min_length=2, max_length=10)
    native_name: Optional[str] = Field(None, max_length=100)
    direction: Optional[str] = Field(None, pattern="^(ltr|rtl)$")
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None

class LanguageResponse(LanguageBase, TimestampSchema):
    id: int
    country_id: Optional[int] = None
    is_active: bool
    is_default: bool