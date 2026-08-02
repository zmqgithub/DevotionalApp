# app/modules/contents/model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base


class ContentType(str, enum.Enum):
    ARTICLE = "article"
    VIDEO = "video"
    AUDIO = "audio"
    PDF = "pdf"
    IMAGE = "image"
    QUIZ = "quiz"
    POEM = "poem"
    PRAYER = "prayer"
    STORY = "story"


class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, index=True, nullable=False)
    subtitle = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Main content body
    content_type = Column(Enum(ContentType), nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)

    # Metadata
    featured_image = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    reading_time = Column(Integer, nullable=True)  # in minutes
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)

    # SEO
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(500), nullable=True)
    meta_keywords = Column(String(500), nullable=True)

    # Settings
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    allow_comments = Column(Boolean, default=True)
    allow_rating = Column(Boolean, default=True)

    # JSON fields for flexible data - RENAMED from 'metadata' to 'extra_data'
    extra_data = Column(JSON, nullable=True)  # Additional structured data
    tags = Column(JSON, nullable=True)  # Array of tags
    translations = Column(JSON, nullable=True)  # Translation mappings

    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    category = relationship("Category", back_populates="contents")
    language = relationship("Language")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])

    recitations = relationship("Recitation", back_populates="content", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="content", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="content", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="content", cascade="all, delete-orphan")
    playlist_items = relationship("PlaylistItem", back_populates="content", cascade="all, delete-orphan")
    dedications = relationship("Dedication", back_populates="content", cascade="all, delete-orphan")
    recent_history = relationship("RecentHistory", back_populates="content", cascade="all, delete-orphan")