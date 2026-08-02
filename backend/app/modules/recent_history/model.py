# app/modules/recent_history/model.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, JSON, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class RecentHistory(Base):
    __tablename__ = "recent_history"

    id = Column(Integer, primary_key=True, index=True)
    progress = Column(Float, default=0)  # % progress
    last_position = Column(Integer, nullable=True)  # For audio/video
    # RENAMED from 'metadata' to 'extra_data'
    extra_data = Column(JSON, nullable=True)  # Additional context

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="recent_history")
    content = relationship("Content", back_populates="recent_history")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'content_id', name='unique_user_content_history'),
    )