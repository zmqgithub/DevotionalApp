# app/modules/favorites/model.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    content = relationship("Content", back_populates="favorites")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'content_id', name='unique_user_content_favorite'),
    )