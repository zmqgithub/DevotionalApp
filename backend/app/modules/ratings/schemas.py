from __future__ import annotations
from pydantic import Field, validator
from typing import Optional
from app.schemas.base import BaseSchema, TimestampSchema

class RatingBase(BaseSchema):
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(None, max_length=1000)

    @validator('rating')
    def validate_rating(cls, v):
        if v not in range(1, 6):
            raise ValueError('Rating must be between 1 and 5')
        return v

class RatingCreate(RatingBase):
    content_id: int

class RatingUpdate(BaseSchema):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review: Optional[str] = Field(None, max_length=1000)

class RatingResponse(RatingBase, TimestampSchema):
    id: int
    user_id: int
    content_id: int
    username: Optional[str] = None
    content_title: Optional[str] = None