# app/modules/announcements/model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    priority = Column(Integer, default=0)  # Higher = more important

    # Targeting
    target_audience = Column(JSON, nullable=True)  # User segments, roles, etc.
    show_from = Column(DateTime(timezone=True), nullable=True)
    show_until = Column(DateTime(timezone=True), nullable=True)

    # Multimedia
    image_url = Column(String(500), nullable=True)
    link_url = Column(String(500), nullable=True)
    # RENAMED from 'metadata' to 'extra_data'
    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])