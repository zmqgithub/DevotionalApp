from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.schedules.repository import ScheduleRepository
from app.modules.schedules.model import Schedule
from app.modules.schedules.schemas import ScheduleCreate, ScheduleUpdate
from app.core.exceptions import ValidationError, NotFoundError


class ScheduleService(BaseService[Schedule, ScheduleCreate, ScheduleUpdate]):
    """Service for Schedule business logic"""

    def __init__(self, db: Session):
        self.repository = ScheduleRepository(db)
        super().__init__(self.repository)

    def get_by_mosque(self, mosque_id: int) -> List[Schedule]:
        """Get all schedules for a mosque"""
        return self.repository.get_by_mosque(mosque_id)

    def get_by_event(self, event_id: int) -> List[Schedule]:
        """Get all schedules for an event"""
        return self.repository.get_by_event(event_id)

    def get_recurring_schedules(self) -> List[Schedule]:
        """Get all recurring schedules"""
        return self.repository.get_recurring_schedules()

    def get_schedules_for_day(self, day_of_week: int) -> List[Schedule]:
        """Get schedules for a specific day of week"""
        if not 0 <= day_of_week <= 6:
            raise ValidationError("Day of week must be between 0 (Monday) and 6 (Sunday)")
        return self.repository.get_schedules_for_day(day_of_week)

    def get_active_schedules_for_mosque(self, mosque_id: int) -> List[Schedule]:
        """Get active schedules for a mosque (recurring + specific dates)"""
        schedules = self.repository.get_by_mosque(mosque_id)

        # Filter: either recurring or upcoming specific date
        now = datetime.utcnow()
        active_schedules = []

        for schedule in schedules:
            if schedule.is_recurring:
                active_schedules.append(schedule)
            elif schedule.date and schedule.date >= now:
                active_schedules.append(schedule)

        return active_schedules

    def _validate_create(self, obj_in: ScheduleCreate) -> None:
        """Validate schedule creation"""
        # Validate time format
        try:
            datetime.strptime(obj_in.start_time, '%H:%M')
        except ValueError:
            raise ValidationError("Start time must be in HH:MM format")

        if obj_in.end_time:
            try:
                datetime.strptime(obj_in.end_time, '%H:%M')
            except ValueError:
                raise ValidationError("End time must be in HH:MM format")

            # Validate end time is after start time
            start = datetime.strptime(obj_in.start_time, '%H:%M')
            end = datetime.strptime(obj_in.end_time, '%H:%M')
            if end <= start:
                raise ValidationError("End time must be after start time")

        # Validate day of week for recurring schedules
        if obj_in.is_recurring and obj_in.day_of_week is None:
            raise ValidationError("Day of week is required for recurring schedules")

        # Validate date for non-recurring schedules
        if not obj_in.is_recurring and obj_in.date is None:
            raise ValidationError("Date is required for non-recurring schedules")