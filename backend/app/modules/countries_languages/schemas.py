from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class CountryLanguageBase(BaseSchema):
    is_primary: bool = False

class CountryLanguageCreate(CountryLanguageBase):
    country_id: int
    language_id: int

class CountryLanguageUpdate(BaseSchema):
    is_primary: Optional[bool] = None

class CountryLanguageResponse(CountryLanguageBase, TimestampSchema):
    id: int
    country_id: int
    language_id: int
    country_name: Optional[str] = None
    language_name: Optional[str] = None