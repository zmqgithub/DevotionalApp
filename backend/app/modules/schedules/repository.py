from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.schedules.model import Schedule
from app.modules.schedules.schemas import ScheduleCreate, ScheduleUpdate


class ScheduleRepository(BaseRepository[Schedule, ScheduleCreate, ScheduleUpdate]):
    """Repository for Schedule model"""

    def __init__(self, db: Session):
        super().__init__(db, Schedule)

    def get_by_mosque(self, mosque_id: int) -> List[Schedule]:
        """Get all schedules for a mosque"""
        return self.db.query(Schedule).filter(
            Schedule.mosque_id == mosque_id
        ).all()

    def get_by_event(self, event_id: int) -> List[Schedule]:
        """Get all schedules for an event"""
        return self.db.query(Schedule).filter(
            Schedule.event_id == event_id
        ).all()

    def get_recurring_schedules(self) -> List[Schedule]:
        """Get all recurring schedules"""
        return self.db.query(Schedule).filter(
            Schedule.is_recurring == True
        ).all()

    def get_schedules_for_day(self, day_of_week: int) -> List[Schedule]:
        """Get schedules for a specific day of week"""
        return self.db.query(Schedule).filter(
            Schedule.day_of_week == day_of_week,
            Schedule.is_recurring == True
        ).all()