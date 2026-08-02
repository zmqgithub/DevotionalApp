from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.roles.repository import RoleRepository
from app.modules.roles.model import Role
from app.modules.roles.schemas import RoleCreate, RoleUpdate
from app.core.exceptions import ValidationError, DuplicateError


class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    """Service for Role business logic"""

    def __init__(self, db: Session):
        self.repository = RoleRepository(db)
        super().__init__(self.repository)

    def get_by_name(self, name: str) -> Optional[Role]:
        """Get role by name"""
        return self.repository.get_by_name(name)

    def get_active_roles(self) -> List[Role]:
        """Get all active roles"""
        return self.repository.get_active_roles()

    def get_system_roles(self) -> List[Role]:
        """Get all system roles"""
        return self.repository.get_system_roles()

    def assign_permission(self, role_id: int, permission_id: int) -> bool:
        """Assign a permission to a role"""
        role = self.get_by_id(role_id)
        if role.is_system:
            raise ValidationError("Cannot modify system role")

        return self.repository.assign_permission(role_id, permission_id)

    def remove_permission(self, role_id: int, permission_id: int) -> bool:
        """Remove a permission from a role"""
        role = self.get_by_id(role_id)
        if role.is_system:
            raise ValidationError("Cannot modify system role")

        return self.repository.remove_permission(role_id, permission_id)

    def _check_duplicate_on_create(self, obj_in: RoleCreate) -> None:
        """Check for duplicate role"""
        if self.repository.get_by_name(obj_in.name):
            raise DuplicateError(f"Role with name {obj_in.name} already exists")

    def _check_duplicate_on_update(self, obj_in: RoleUpdate, id: int) -> None:
        """Check for duplicate role on update"""
        if hasattr(obj_in, 'name') and obj_in.name:
            existing = self.repository.get_by_name(obj_in.name)
            if existing and existing.id != id:
                raise DuplicateError(f"Role with name {obj_in.name} already exists")

    def _validate_delete(self, id: int) -> None:
        """Validate role deletion"""
        role = self.get_by_id(id)
        if role.is_system:
            raise ValidationError("Cannot delete system role")