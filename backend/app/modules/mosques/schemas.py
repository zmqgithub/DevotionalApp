from __future__ import annotations
from pydantic import Field, validator
from typing import Optional, List, Any
from app.schemas.base import BaseSchema, TimestampSchema


class MosqueBase(BaseSchema):
    name: str = Field(..., max_length=255)
    arabic_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    address: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = None
    has_parking: bool = False
    has_wudu_area: bool = True
    has_women_area: bool = True
    has_handicap_access: bool = False
    has_library: bool = False
    images: Optional[List[str]] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    denomination: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, max_length=50)

    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v


class MosqueCreate(MosqueBase):
    city_id: int


class MosqueUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=255)
    arabic_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = None
    has_parking: Optional[bool] = None
    has_wudu_area: Optional[bool] = None
    has_women_area: Optional[bool] = None
    has_handicap_access: Optional[bool] = None
    has_library: Optional[bool] = None
    images: Optional[List[str]] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    denomination: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class MosqueResponse(MosqueBase, TimestampSchema):
    id: int
    city_id: int
    created_by: Optional[int] = None
    is_active: bool
    is_verified: bool