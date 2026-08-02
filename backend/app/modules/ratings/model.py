# app/modules/ratings/model.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="ratings")
    content = relationship("Content", back_populates="ratings")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'content_id', name='unique_user_content_rating'),
    )