from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class CityBase(BaseSchema):
    name: str = Field(..., max_length=100)
    city_code: Optional[str] = Field(None, max_length=20)
    type: Optional[str] = Field(None, max_length=50)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    is_capital: bool = False

class CityCreate(CityBase):
    state_id: int

class CityUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    city_code: Optional[str] = Field(None, max_length=20)
    type: Optional[str] = Field(None, max_length=50)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    is_capital: Optional[bool] = None
    is_active: Optional[bool] = None

class CityResponse(CityBase, TimestampSchema):
    id: int
    state_id: int
    is_active: bool