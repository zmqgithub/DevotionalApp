from pydantic import Field
from typing import Optional, List
from app.schemas.base import BaseSchema, TimestampSchema

class CountryBase(BaseSchema):
    name: str = Field(..., max_length=100)
    iso_code: str = Field(..., min_length=2, max_length=2)
    iso3_code: Optional[str] = Field(None, min_length=3, max_length=3)
    phone_code: Optional[str] = Field(None, max_length=10)
    currency_code: Optional[str] = Field(None, max_length=3)
    currency_name: Optional[str] = Field(None, max_length=50)
    region: Optional[str] = Field(None, max_length=100)
    subregion: Optional[str] = Field(None, max_length=100)
    capital: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    flag: Optional[str] = Field(None, max_length=200)

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    iso_code: Optional[str] = Field(None, min_length=2, max_length=2)
    iso3_code: Optional[str] = Field(None, min_length=3, max_length=3)
    phone_code: Optional[str] = Field(None, max_length=10)
    currency_code: Optional[str] = Field(None, max_length=3)
    currency_name: Optional[str] = Field(None, max_length=50)
    region: Optional[str] = Field(None, max_length=100)
    subregion: Optional[str] = Field(None, max_length=100)
    capital: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    flag: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None

class CountryResponse(CountryBase, TimestampSchema):
    id: int
    is_active: bool