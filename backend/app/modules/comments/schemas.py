from __future__ import annotations
from pydantic import Field
from typing import Optional, List
from app.schemas.base import BaseSchema, TimestampSchema


class CommentBase(BaseSchema):
    content: str = Field(..., max_length=5000)


class CommentCreate(CommentBase):
    content_id: int
    parent_id: Optional[int] = None


class CommentUpdate(BaseSchema):
    content: Optional[str] = Field(None, max_length=5000)


class CommentResponse(CommentBase, TimestampSchema):
    id: int
    user_id: int
    content_id: int
    parent_id: Optional[int] = None
    is_approved: bool
    is_pinned: bool
    like_count: int

    username: Optional[str] = None
    user_profile_picture: Optional[str] = None
    replies: List['CommentResponse'] = []