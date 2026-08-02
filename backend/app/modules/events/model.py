# app/modules/events/model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base


class EventType(str, enum.Enum):
    PRAYER = "prayer"
    LECTURE = "lecture"
    CLASS = "class"
    COMMUNITY = "community"
    SPECIAL = "special"
    OTHER = "other"


class EventStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(Enum(EventType), nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.UPCOMING)

    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # Location
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_virtual = Column(Boolean, default=False)
    virtual_link = Column(String(500), nullable=True)

    # Additional info
    capacity = Column(Integer, nullable=True)
    registered_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    requires_registration = Column(Boolean, default=False)

    # Multimedia - RENAMED from 'metadata' to 'extra_data'
    featured_image = Column(String(500), nullable=True)
    images = Column(JSON, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Changed from 'metadata'

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    mosque_id = Column(Integer, ForeignKey("mosques.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    mosque = relationship("Mosque", back_populates="events")
    schedules = relationship("Schedule", back_populates="event", cascade="all, delete-orphan")