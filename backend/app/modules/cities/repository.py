from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.cities.model import City
from app.modules.cities.schemas import CityCreate, CityUpdate


class CityRepository(BaseRepository[City, CityCreate, CityUpdate]):
    """Repository for City model"""

    def __init__(self, db: Session):
        super().__init__(db, City)

    def get_by_state(self, state_id: int) -> List[City]:
        """Get all cities in a state"""
        return self.db.query(City).filter(
            City.state_id == state_id,
            City.is_active == True
        ).all()

    def get_by_name_and_state(self, name: str, state_id: int) -> Optional[City]:
        """Get city by name and state"""
        return self.db.query(City).filter(
            City.name.ilike(name),
            City.state_id == state_id
        ).first()

    def search_cities(self, search: str) -> List[City]:
        """Search cities by name"""
        return self.db.query(City).filter(
            City.name.ilike(f"%{search}%"),
            City.is_active == True
        ).all()

    def get_capital_cities(self) -> List[City]:
        """Get all capital cities"""
        return self.db.query(City).filter(
            City.is_capital == True,
            City.is_active == True
        ).all()

    def get_city_with_mosques(self, city_id: int) -> Optional[City]:
        """Get city with its mosques"""
        return self.db.query(City).filter(City.id == city_id).first()