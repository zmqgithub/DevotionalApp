from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.repositories.base import BaseRepository
from app.modules.countries.model import Country
from app.modules.countries.schemas import CountryCreate, CountryUpdate


class CountryRepository(BaseRepository[Country, CountryCreate, CountryUpdate]):
    """Repository for Country model"""

    def __init__(self, db: Session):
        super().__init__(db, Country)

    def get_by_iso_code(self, iso_code: str) -> Optional[Country]:
        """Get country by ISO code"""
        return self.db.query(Country).filter(Country.iso_code == iso_code.upper()).first()

    def get_by_name(self, name: str) -> Optional[Country]:
        """Get country by name"""
        return self.db.query(Country).filter(Country.name.ilike(name)).first()

    def search_countries(self, search: str) -> List[Country]:
        """Search countries by name or ISO code"""
        return self.db.query(Country).filter(
            or_(
                Country.name.ilike(f"%{search}%"),
                Country.iso_code.ilike(f"%{search}%"),
                Country.iso3_code.ilike(f"%{search}%")
            )
        ).all()

    def get_active_countries(self) -> List[Country]:
        """Get all active countries"""
        return self.db.query(Country).filter(Country.is_active == True).all()

    def get_country_with_states(self, country_id: int) -> Optional[Country]:
        """Get country with its states"""
        return self.db.query(Country).filter(Country.id == country_id).first()