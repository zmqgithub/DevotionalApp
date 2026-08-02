# app/modules/playlists/playlist_items/model.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class PlaylistItem(Base):
    __tablename__ = "playlist_items"

    id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, default=0)
    notes = Column(JSON, nullable=True)  # User notes for this item

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    # Relationships
    playlist = relationship("Playlist", back_populates="items")
    content = relationship("Content", back_populates="playlist_items")