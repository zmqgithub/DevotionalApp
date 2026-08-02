from __future__ import annotations
from pydantic import Field, validator
from typing import Optional, List
from app.schemas.base import BaseSchema, TimestampSchema

class CategoryBase(BaseSchema):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=200)
    color: Optional[str] = Field(None, max_length=50)
    order: int = 0

    @validator('slug')
    def validate_slug(cls, v):
        if not v.replace('-', '').isalnum():
            raise ValueError('Slug must be alphanumeric with hyphens only')
        return v.lower()

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

class CategoryUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=200)
    color: Optional[str] = Field(None, max_length=50)
    parent_id: Optional[int] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase, TimestampSchema):
    id: int
    parent_id: Optional[int] = None
    is_active: bool

class CategoryWithChildrenResponse(CategoryResponse):
    children: List['CategoryResponse'] = []