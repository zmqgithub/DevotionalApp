# app/modules/recitations/model.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Recitation(Base):
    __tablename__ = "recitations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    audio_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    duration = Column(Float, nullable=True)  # in seconds
    transcript = Column(Text, nullable=True)
    translation = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False)
    order = Column(Integer, default=0)

    # RENAMED from 'metadata' to 'extra_data'
    extra_data = Column(JSON, nullable=True)  # Additional data like tafsir, etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=True)

    # Relationships
    content = relationship("Content", back_populates="recitations")
    language = relationship("Language")