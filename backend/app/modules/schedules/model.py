# app/modules/schedules/model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=True)  # 0-6 (Monday-Sunday)
    date = Column(DateTime, nullable=True)  # For specific date events
    start_time = Column(String(10), nullable=False)  # HH:MM format
    end_time = Column(String(10), nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(JSON, nullable=True)  # RRULE or custom JSON
    notes = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    mosque_id = Column(Integer, ForeignKey("mosques.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    # Relationships
    mosque = relationship("Mosque", back_populates="schedules")
    event = relationship("Event", back_populates="schedules")