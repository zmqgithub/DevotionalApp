from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.states.repository import StateRepository
from app.modules.states.model import State
from app.modules.states.schemas import StateCreate, StateUpdate
from app.core.exceptions import DuplicateError, NotFoundError


class StateService(BaseService[State, StateCreate, StateUpdate]):
    """Service for State business logic"""

    def __init__(self, db: Session):
        self.repository = StateRepository(db)
        super().__init__(self.repository)

    def get_by_country(self, country_id: int) -> List[State]:
        """Get all states in a country"""
        return self.repository.get_by_country(country_id)

    def get_by_name_and_country(self, name: str, country_id: int) -> Optional[State]:
        """Get state by name and country"""
        return self.repository.get_by_name_and_country(name, country_id)

    def search_states(self, search: str) -> List[State]:
        """Search states by name"""
        return self.repository.search_states(search)

    def get_state_with_cities(self, state_id: int) -> State:
        """Get state with its cities"""
        state = self.repository.get_state_with_cities(state_id)
        if not state:
            raise NotFoundError(f"State with ID {state_id} not found")
        return state

    def _check_duplicate_on_create(self, obj_in: StateCreate) -> None:
        """Check for duplicate state"""
        if self.repository.get_by_name_and_country(obj_in.name, obj_in.country_id):
            raise DuplicateError(f"State with name {obj_in.name} already exists in this country")

    def _check_duplicate_on_update(self, obj_in: StateUpdate, id: int) -> None:
        """Check for duplicate state on update"""
        if hasattr(obj_in, 'name') and obj_in.name and hasattr(obj_in, 'country_id') and obj_in.country_id:
            existing = self.repository.get_by_name_and_country(obj_in.name, obj_in.country_id)
            if existing and existing.id != id:
                raise DuplicateError(f"State with name {obj_in.name} already exists in this country")