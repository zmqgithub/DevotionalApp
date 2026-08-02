from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.cities.repository import CityRepository
from app.modules.cities.model import City
from app.modules.cities.schemas import CityCreate, CityUpdate
from app.core.exceptions import DuplicateError, NotFoundError


class CityService(BaseService[City, CityCreate, CityUpdate]):
    """Service for City business logic"""

    def __init__(self, db: Session):
        self.repository = CityRepository(db)
        super().__init__(self.repository)

    def get_by_state(self, state_id: int) -> List[City]:
        """Get all cities in a state"""
        return self.repository.get_by_state(state_id)

    def get_by_name_and_state(self, name: str, state_id: int) -> Optional[City]:
        """Get city by name and state"""
        return self.repository.get_by_name_and_state(name, state_id)

    def search_cities(self, search: str) -> List[City]:
        """Search cities by name"""
        return self.repository.search_cities(search)

    def get_capital_cities(self) -> List[City]:
        """Get all capital cities"""
        return self.repository.get_capital_cities()

    def get_city_with_mosques(self, city_id: int) -> City:
        """Get city with its mosques"""
        city = self.repository.get_city_with_mosques(city_id)
        if not city:
            raise NotFoundError(f"City with ID {city_id} not found")
        return city

    def _check_duplicate_on_create(self, obj_in: CityCreate) -> None:
        """Check for duplicate city"""
        if self.repository.get_by_name_and_state(obj_in.name, obj_in.state_id):
            raise DuplicateError(f"City with name {obj_in.name} already exists in this state")

    def _check_duplicate_on_update(self, obj_in: CityUpdate, id: int) -> None:
        """Check for duplicate city on update"""
        if hasattr(obj_in, 'name') and obj_in.name and hasattr(obj_in, 'state_id') and obj_in.state_id:
            existing = self.repository.get_by_name_and_state(obj_in.name, obj_in.state_id)
            if existing and existing.id != id:
                raise DuplicateError(f"City with name {obj_in.name} already exists in this state")