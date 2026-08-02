from __future__ import annotations
# app/modules/users/schema.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from enum import Enum
from app.schemas.base import BaseSchema, TimestampSchema


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(BaseSchema):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=500)
    profile_picture: Optional[str] = Field(None, max_length=500)
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None

    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric with underscores only')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v


class UserUpdate(BaseSchema):
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=500)
    profile_picture: Optional[str] = Field(None, max_length=500)
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None


class UserResponse(UserBase, TimestampSchema):
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool
    status: UserStatus
    last_login: Optional[datetime] = None


class UserProfileResponse(UserResponse):
    roles: List[str] = []
    permissions: List[str] = []