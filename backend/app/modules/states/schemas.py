from __future__ import annotations
from pydantic import Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class StateBase(BaseSchema):
    name: str = Field(..., max_length=100)
    state_code: Optional[str] = Field(None, max_length=10)
    type: Optional[str] = Field(None, max_length=50)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class StateCreate(StateBase):
    country_id: int

class StateUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    state_code: Optional[str] = Field(None, max_length=10)
    type: Optional[str] = Field(None, max_length=50)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None

class StateResponse(StateBase, TimestampSchema):
    id: int
    country_id: int
    is_active: bool