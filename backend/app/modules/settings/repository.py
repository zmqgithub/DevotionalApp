from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.settings.model import Setting
from app.modules.settings.schema import SettingsCreate, SettingsUpdate


class SettingsRepository(BaseRepository[Setting, SettingsCreate, SettingsUpdate]):
    """Repository for Settings model"""

    def __init__(self, db: Session):
        super().__init__(db, Setting)

    def get_by_user(self, user_id: int) -> Optional[Setting]:
        """Get settings for a user"""
        return self.db.query(Setting).filter(Setting.user_id == user_id).first()

    def create_or_update(self, user_id: int, settings_data: dict) -> Setting:
        """Create or update settings for a user"""
        settings = self.get_by_user(user_id)

        if settings:
            # Update existing
            for key, value in settings_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
        else:
            # Create new
            settings = Setting(user_id=user_id, **settings_data)
            self.db.add(settings)

        self.db.commit()
        self.db.refresh(settings)
        return settings