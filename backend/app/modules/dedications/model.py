# app/modules/dedications/model.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Dedication(Base):
    __tablename__ = "dedications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="dedications")
    content = relationship("Content", back_populates="dedications")