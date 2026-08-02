from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.mosques.repository import MosqueRepository
from app.modules.mosques.model import Mosque
from app.modules.mosques.schemas import MosqueCreate, MosqueUpdate
from app.core.exceptions import ValidationError, NotFoundError


class MosqueService(BaseService[Mosque, MosqueCreate, MosqueUpdate]):
    """Service for Mosque business logic"""

    def __init__(self, db: Session):
        self.repository = MosqueRepository(db)
        super().__init__(self.repository)

    def get_by_city(self, city_id: int) -> List[Mosque]:
        """Get all mosques in a city"""
        return self.repository.get_by_city(city_id)

    def get_by_location(self, latitude: float, longitude: float, radius_km: float = 10) -> List[Mosque]:
        """Get mosques within a radius (in km)"""
        # Validate coordinates
        if not -90 <= latitude <= 90:
            raise ValidationError("Latitude must be between -90 and 90")
        if not -180 <= longitude <= 180:
            raise ValidationError("Longitude must be between -180 and 180")
        if radius_km <= 0:
            raise ValidationError("Radius must be greater than 0")

        return self.repository.get_by_location(latitude, longitude, radius_km)

    def get_verified_mosques(self) -> List[Mosque]:
        """Get all verified mosques"""
        return self.repository.get_verified_mosques()

    def search_mosques(self, search: str) -> List[Mosque]:
        """Search mosques by name or address"""
        if len(search) < 2:
            raise ValidationError("Search term must be at least 2 characters")
        return self.repository.search_mosques(search)

    def verify_mosque(self, mosque_id: int) -> Mosque:
        """Verify a mosque"""
        mosque = self.get_by_id(mosque_id)
        if mosque.is_verified:
            raise ValidationError("Mosque is already verified")

        return self.repository.verify_mosque(mosque_id)

    def _validate_create(self, obj_in: MosqueCreate) -> None:
        """Validate mosque creation"""
        # Validate coordinates
        if not -90 <= obj_in.latitude <= 90:
            raise ValidationError("Latitude must be between -90 and 90")
        if not -180 <= obj_in.longitude <= 180:
            raise ValidationError("Longitude must be between -180 and 180")