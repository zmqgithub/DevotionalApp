from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.states.model import State
from app.modules.states.schemas import StateCreate, StateUpdate


class StateRepository(BaseRepository[State, StateCreate, StateUpdate]):
    """Repository for State model"""

    def __init__(self, db: Session):
        super().__init__(db, State)

    def get_by_country(self, country_id: int) -> List[State]:
        """Get all states in a country"""
        return self.db.query(State).filter(
            State.country_id == country_id,
            State.is_active == True
        ).all()

    def get_by_name_and_country(self, name: str, country_id: int) -> Optional[State]:
        """Get state by name and country"""
        return self.db.query(State).filter(
            State.name.ilike(name),
            State.country_id == country_id
        ).first()

    def search_states(self, search: str) -> List[State]:
        """Search states by name"""
        return self.db.query(State).filter(
            State.name.ilike(f"%{search}%"),
            State.is_active == True
        ).all()

    def get_state_with_cities(self, state_id: int) -> Optional[State]:
        """Get state with its cities"""
        return self.db.query(State).filter(State.id == state_id).first()