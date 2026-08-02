from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.repositories.base import BaseRepository
from app.modules.mosques.model import Mosque
from app.modules.mosques.schemas import MosqueCreate, MosqueUpdate


class MosqueRepository(BaseRepository[Mosque, MosqueCreate, MosqueUpdate]):
    """Repository for Mosque model"""

    def __init__(self, db: Session):
        super().__init__(db, Mosque)

    def get_by_city(self, city_id: int) -> List[Mosque]:
        """Get all mosques in a city"""
        return self.db.query(Mosque).filter(
            Mosque.city_id == city_id,
            Mosque.is_active == True
        ).all()

    def get_by_location(self, latitude: float, longitude: float, radius_km: float = 10) -> List[Mosque]:
        """Get mosques within a radius (in km)"""
        # Simplified: in production, use PostGIS or proper geospatial queries
        return self.db.query(Mosque).filter(
            Mosque.is_active == True,
            Mosque.latitude.between(latitude - 0.1, latitude + 0.1),
            Mosque.longitude.between(longitude - 0.1, longitude + 0.1)
        ).all()

    def get_verified_mosques(self) -> List[Mosque]:
        """Get all verified mosques"""
        return self.db.query(Mosque).filter(
            Mosque.is_verified == True,
            Mosque.is_active == True
        ).all()

    def search_mosques(self, search: str) -> List[Mosque]:
        """Search mosques by name or address"""
        return self.db.query(Mosque).filter(
            or_(
                Mosque.name.ilike(f"%{search}%"),
                Mosque.address.ilike(f"%{search}%")
            ),
            Mosque.is_active == True
        ).all()

    def verify_mosque(self, mosque_id: int) -> Optional[Mosque]:
        """Verify a mosque"""
        mosque = self.get_by_id(mosque_id)
        if mosque:
            mosque.is_verified = True
            self.db.commit()
            self.db.refresh(mosque)
        return mosque