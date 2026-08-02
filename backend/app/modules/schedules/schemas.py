from __future__ import annotations
from pydantic import Field, validator
from typing import Optional, Any
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampSchema

class ScheduleBase(BaseSchema):
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    date: Optional[datetime] = None
    start_time: str = Field(..., pattern=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    end_time: Optional[str] = Field(None, pattern=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    is_recurring: bool = False
    recurrence_rule: Optional[Any] = None
    notes: Optional[str] = Field(None, max_length=500)

    @validator('end_time')
    def validate_times(cls, v, values):
        if v and 'start_time' in values:
            start = values['start_time']
            if start and v <= start:
                raise ValueError('End time must be after start time')
        return v

class ScheduleCreate(ScheduleBase):
    mosque_id: int
    event_id: Optional[int] = None

class ScheduleUpdate(BaseSchema):
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    date: Optional[datetime] = None
    start_time: Optional[str] = Field(None, pattern=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    end_time: Optional[str] = Field(None, pattern=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[Any] = None
    notes: Optional[str] = Field(None, max_length=500)

class ScheduleResponse(ScheduleBase, TimestampSchema):
    id: int
    mosque_id: int
    event_id: Optional[int] = None