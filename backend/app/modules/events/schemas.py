from __future__ import annotations
from pydantic import Field, validator
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum
from app.schemas.base import BaseSchema, TimestampSchema

class EventType(str, Enum):
    PRAYER = "prayer"
    LECTURE = "lecture"
    CLASS = "class"
    COMMUNITY = "community"
    SPECIAL = "special"
    OTHER = "other"

class EventStatus(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EventBase(BaseSchema):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    event_type: EventType
    start_date: datetime
    end_date: Optional[datetime] = None
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_virtual: bool = False
    virtual_link: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = None
    is_featured: bool = False
    requires_registration: bool = False
    featured_image: Optional[str] = Field(None, max_length=500)
    images: Optional[List[str]] = None
    extra_data: Optional[Any] = None

    @validator('end_date')
    def validate_dates(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class EventCreate(EventBase):
    mosque_id: int

class EventUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    event_type: Optional[EventType] = None
    status: Optional[EventStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_virtual: Optional[bool] = None
    virtual_link: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = None
    is_featured: Optional[bool] = None
    requires_registration: Optional[bool] = None
    featured_image: Optional[str] = Field(None, max_length=500)
    images: Optional[List[str]] = None
    extra_data: Optional[Any] = None

class EventResponse(EventBase, TimestampSchema):
    id: int
    mosque_id: int
    created_by: Optional[int] = None
    status: EventStatus
    registered_count: int