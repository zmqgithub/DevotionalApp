from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.languages.repository import LanguageRepository
from app.modules.languages.model import Language
from app.modules.languages.schemas import LanguageCreate, LanguageUpdate
from app.core.exceptions import DuplicateError, ValidationError


class LanguageService(BaseService[Language, LanguageCreate, LanguageUpdate]):
    """Service for Language business logic"""

    def __init__(self, db: Session):
        self.repository = LanguageRepository(db)
        super().__init__(self.repository)

    def get_by_code(self, code: str) -> Optional[Language]:
        """Get language by code"""
        return self.repository.get_by_code(code)

    def get_by_name(self, name: str) -> Optional[Language]:
        """Get language by name"""
        return self.repository.get_by_name(name)

    def get_active_languages(self) -> List[Language]:
        """Get all active languages"""
        return self.repository.get_active_languages()

    def get_default_language(self) -> Optional[Language]:
        """Get the default language"""
        return self.repository.get_default_language()

    def get_languages_by_country(self, country_id: int) -> List[Language]:
        """Get languages spoken in a country"""
        return self.repository.get_languages_by_country(country_id)

    def set_default_language(self, language_id: int) -> Language:
        """Set a language as default"""
        # Get current default
        current_default = self.repository.get_default_language()
        if current_default:
            # Unset current default
            self.repository.update(current_default.id, {"is_default": False})

        # Set new default
        language = self.get_by_id(language_id)
        return self.repository.update(language_id, {"is_default": True})

    def _check_duplicate_on_create(self, obj_in: LanguageCreate) -> None:
        """Check for duplicate language"""
        if self.repository.get_by_code(obj_in.code):
            raise DuplicateError(f"Language with code {obj_in.code} already exists")

        if self.repository.get_by_name(obj_in.name):
            raise DuplicateError(f"Language with name {obj_in.name} already exists")

    def _check_duplicate_on_update(self, obj_in: LanguageUpdate, id: int) -> None:
        """Check for duplicate language on update"""
        if hasattr(obj_in, 'code') and obj_in.code:
            existing = self.repository.get_by_code(obj_in.code)
            if existing and existing.id != id:
                raise DuplicateError(f"Language with code {obj_in.code} already exists")

        if hasattr(obj_in, 'name') and obj_in.name:
            existing = self.repository.get_by_name(obj_in.name)
            if existing and existing.id != id:
                raise DuplicateError(f"Language with name {obj_in.name} already exists")