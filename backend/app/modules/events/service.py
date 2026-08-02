from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.events.repository import EventRepository
from app.modules.events.model import Event, EventStatus
from app.modules.events.schemas import EventCreate, EventUpdate
from app.core.exceptions import ValidationError, NotFoundError


class EventService(BaseService[Event, EventCreate, EventUpdate]):
    """Service for Event business logic"""

    def __init__(self, db: Session):
        self.repository = EventRepository(db)
        super().__init__(self.repository)

    def get_by_mosque(self, mosque_id: int) -> List[Event]:
        """Get all events at a mosque"""
        return self.repository.get_by_mosque(mosque_id)

    def get_upcoming_events(self, days: int = 30) -> List[Event]:
        """Get upcoming events"""
        if days <= 0:
            raise ValidationError("Days must be greater than 0")
        return self.repository.get_upcoming_events(days)

    def get_ongoing_events(self) -> List[Event]:
        """Get ongoing events"""
        return self.repository.get_ongoing_events()

    def get_events_by_date(self, date: datetime) -> List[Event]:
        """Get events on a specific date"""
        return self.repository.get_events_by_date(date)

    def get_featured_events(self, limit: int = 10) -> List[Event]:
        """Get featured events"""
        if limit <= 0:
            raise ValidationError("Limit must be greater than 0")
        return self.repository.get_featured_events(limit)

    def register_for_event(self, event_id: int) -> Event:
        """Register for an event"""
        event = self.get_by_id(event_id)

        if event.status != EventStatus.UPCOMING:
            raise ValidationError(f"Event is not open for registration (status: {event.status})")

        if event.capacity and event.registered_count >= event.capacity:
            raise ValidationError("Event has reached maximum capacity")

        self.repository.register_for_event(event_id)
        return self.get_by_id(event_id)

    def update_event_status(self, event_id: int) -> Event:
        """Update event status based on current time"""
        event = self.get_by_id(event_id)
        now = datetime.utcnow()

        if event.start_date <= now <= event.end_date:
            event.status = EventStatus.ONGOING
        elif event.end_date < now:
            event.status = EventStatus.COMPLETED

        return self.repository.update(event_id, event)

    def _validate_create(self, obj_in: EventCreate) -> None:
        """Validate event creation"""
        if obj_in.start_date < datetime.utcnow():
            raise ValidationError("Start date cannot be in the past")

        if obj_in.end_date and obj_in.end_date <= obj_in.start_date:
            raise ValidationError("End date must be after start date")

        if obj_in.capacity and obj_in.capacity < 0:
            raise ValidationError("Capacity cannot be negative")