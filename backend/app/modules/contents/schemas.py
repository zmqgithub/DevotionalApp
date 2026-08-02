from __future__ import annotations

from pydantic import Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from app.schemas.base import BaseSchema, TimestampSchema


class ContentType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    AUDIO = "audio"
    PDF = "pdf"
    IMAGE = "image"
    QUIZ = "quiz"
    POEM = "poem"
    PRAYER = "prayer"
    STORY = "story"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class ContentBase(BaseSchema):
    title: str = Field(..., max_length=500)
    slug: str = Field(..., max_length=500)
    subtitle: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    content: Optional[str] = None
    content_type: ContentType
    status: ContentStatus = ContentStatus.DRAFT

    # Metadata
    featured_image: Optional[str] = Field(None, max_length=500)
    audio_url: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=500)
    duration: Optional[int] = None
    reading_time: Optional[int] = None

    # SEO
    meta_title: Optional[str] = Field(None, max_length=200)
    meta_description: Optional[str] = Field(None, max_length=500)
    meta_keywords: Optional[str] = Field(None, max_length=500)

    # Settings
    is_featured: bool = False
    is_premium: bool = False
    allow_comments: bool = True
    allow_rating: bool = True

    # JSON fields
    tags: Optional[List[str]] = None
    translations: Optional[Dict[str, Any]] = None
    extra_data: Optional[Dict[str, Any]] = None

    @validator('slug')
    def validate_slug(cls, v):
        if not v.replace('-', '').isalnum():
            raise ValueError('Slug must be alphanumeric with hyphens only')
        return v.lower()


class ContentCreate(ContentBase):
    category_id: int
    language_id: Optional[int] = None


class ContentUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=500)
    slug: Optional[str] = Field(None, max_length=500)
    subtitle: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[ContentType] = None
    status: Optional[ContentStatus] = None
    featured_image: Optional[str] = Field(None, max_length=500)
    audio_url: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=500)
    duration: Optional[int] = None
    reading_time: Optional[int] = None
    meta_title: Optional[str] = Field(None, max_length=200)
    meta_description: Optional[str] = Field(None, max_length=500)
    meta_keywords: Optional[str] = Field(None, max_length=500)
    is_featured: Optional[bool] = None
    is_premium: Optional[bool] = None
    allow_comments: Optional[bool] = None
    allow_rating: Optional[bool] = None
    tags: Optional[List[str]] = None
    translations: Optional[Dict[str, Any]] = None
    extra_data: Optional[Dict[str, Any]] = None
    category_id: Optional[int] = None
    language_id: Optional[int] = None
    published_at: Optional[datetime] = None


class ContentResponse(ContentBase, TimestampSchema):
    id: int
    category_id: int
    language_id: Optional[int] = None
    created_by: int
    updated_by: Optional[int] = None
    view_count: int
    like_count: int
    share_count: int
    published_at: Optional[datetime] = None

    # Additional fields from relationships
    creator_username: Optional[str] = None
    category_name: Optional[str] = None
    average_rating: Optional[float] = None
    total_ratings: Optional[int] = None
    total_comments: Optional[int] = None


# Use forward references with strings
class ContentDetailResponse(ContentResponse):
    recitations: Optional[List['RecitationResponse']] = None
    comments: Optional[List['CommentResponse']] = None
    ratings: Optional[List['RatingResponse']] = None


# Define the referenced classes after they're used
# These will be resolved at runtime due to __future__ import
class RecitationResponse(BaseSchema):
    id: int
    title: str
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[float] = None
    order: int
    is_published: bool


class CommentResponse(BaseSchema):
    id: int
    user_id: int
    content_id: int
    parent_id: Optional[int] = None
    content: str
    is_approved: bool
    is_pinned: bool
    like_count: int
    created_at: datetime
    username: Optional[str] = None
    user_profile_picture: Optional[str] = None
    replies: Optional[List['CommentResponse']] = None


class RatingResponse(BaseSchema):
    id: int
    user_id: int
    content_id: int
    rating: int
    review: Optional[str] = None
    created_at: datetime
    username: Optional[str] = None


# Rebuild the model to resolve forward references
ContentDetailResponse.model_rebuild()
CommentResponse.model_rebuild()