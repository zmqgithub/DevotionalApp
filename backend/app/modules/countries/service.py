from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.countries.repository import CountryRepository
from app.modules.countries.model import Country
from app.modules.countries.schemas import CountryCreate, CountryUpdate
from app.core.exceptions import DuplicateError


class CountryService(BaseService[Country, CountryCreate, CountryUpdate]):
    """Service for Country business logic"""

    def __init__(self, db: Session):
        self.repository = CountryRepository(db)
        super().__init__(self.repository)

    def get_by_iso_code(self, iso_code: str) -> Optional[Country]:
        """Get country by ISO code"""
        return self.repository.get_by_iso_code(iso_code)

    def get_by_name(self, name: str) -> Optional[Country]:
        """Get country by name"""
        return self.repository.get_by_name(name)

    def search_countries(self, search: str) -> List[Country]:
        """Search countries"""
        return self.repository.search_countries(search)

    def get_active_countries(self) -> List[Country]:
        """Get all active countries"""
        return self.repository.get_active_countries()

    def get_country_with_states(self, country_id: int) -> Country:
        """Get country with its states"""
        country = self.repository.get_country_with_states(country_id)
        if not country:
            raise NotFoundError(f"Country with ID {country_id} not found")
        return country

    def _check_duplicate_on_create(self, obj_in: CountryCreate) -> None:
        """Check for duplicate country"""
        if self.repository.get_by_iso_code(obj_in.iso_code):
            raise DuplicateError(f"Country with ISO code {obj_in.iso_code} already exists")

        if self.repository.get_by_name(obj_in.name):
            raise DuplicateError(f"Country with name {obj_in.name} already exists")