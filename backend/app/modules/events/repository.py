from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.events.model import Event, EventStatus
from app.modules.events.schemas import EventCreate, EventUpdate


class EventRepository(BaseRepository[Event, EventCreate, EventUpdate]):
    """Repository for Event model"""

    def __init__(self, db: Session):
        super().__init__(db, Event)

    def get_by_mosque(self, mosque_id: int) -> List[Event]:
        """Get all events at a mosque"""
        return self.db.query(Event).filter(Event.mosque_id == mosque_id).all()

    def get_upcoming_events(self, days: int = 30) -> List[Event]:
        """Get upcoming events"""
        now = datetime.utcnow()
        future = now + timedelta(days=days)

        return self.db.query(Event).filter(
            Event.start_date >= now,
            Event.start_date <= future,
            Event.status == EventStatus.UPCOMING
        ).order_by(Event.start_date).all()

    def get_ongoing_events(self) -> List[Event]:
        """Get ongoing events"""
        now = datetime.utcnow()
        return self.db.query(Event).filter(
            Event.start_date <= now,
            Event.end_date >= now,
            Event.status == EventStatus.ONGOING
        ).all()

    def get_events_by_date(self, date: datetime) -> List[Event]:
        """Get events on a specific date"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        return self.db.query(Event).filter(
            Event.start_date >= start_of_day,
            Event.start_date <= end_of_day
        ).all()

    def get_featured_events(self, limit: int = 10) -> List[Event]:
        """Get featured events"""
        return self.db.query(Event).filter(
            Event.is_featured == True,
            Event.status == EventStatus.UPCOMING
        ).order_by(Event.start_date).limit(limit).all()

    def register_for_event(self, event_id: int) -> bool:
        """Increment registration count for an event"""
        event = self.get_by_id(event_id)
        if event:
            event.registered_count += 1
            self.db.commit()
            return True
        return False