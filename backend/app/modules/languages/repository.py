from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.languages.model import Language
from app.modules.languages.schemas import LanguageCreate, LanguageUpdate


class LanguageRepository(BaseRepository[Language, LanguageCreate, LanguageUpdate]):
    """Repository for Language model"""

    def __init__(self, db: Session):
        super().__init__(db, Language)

    def get_by_code(self, code: str) -> Optional[Language]:
        """Get language by code"""
        return self.db.query(Language).filter(Language.code == code).first()

    def get_by_name(self, name: str) -> Optional[Language]:
        """Get language by name"""
        return self.db.query(Language).filter(Language.name.ilike(name)).first()

    def get_active_languages(self) -> List[Language]:
        """Get all active languages"""
        return self.db.query(Language).filter(Language.is_active == True).all()

    def get_default_language(self) -> Optional[Language]:
        """Get the default language"""
        return self.db.query(Language).filter(Language.is_default == True).first()

    def get_languages_by_country(self, country_id: int) -> List[Language]:
        """Get languages spoken in a country"""
        return self.db.query(Language).filter(Language.country_id == country_id).all()