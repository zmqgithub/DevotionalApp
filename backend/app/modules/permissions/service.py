from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.permissions.repository import PermissionRepository
from app.modules.permissions.model import Permission
from app.modules.permissions.schemas import PermissionCreate, PermissionUpdate
from app.core.exceptions import DuplicateError


class PermissionService(BaseService[Permission, PermissionCreate, PermissionUpdate]):
    """Service for Permission business logic"""

    def __init__(self, db: Session):
        self.repository = PermissionRepository(db)
        super().__init__(self.repository)

    def get_by_name(self, name: str) -> Optional[Permission]:
        """Get permission by name"""
        return self.repository.get_by_name(name)

    def get_by_resource(self, resource: str) -> List[Permission]:
        """Get permissions by resource"""
        return self.repository.get_by_resource(resource)

    def get_by_action(self, action: str) -> List[Permission]:
        """Get permissions by action"""
        return self.repository.get_by_action(action)

    def get_by_resource_and_action(self, resource: str, action: str) -> Optional[Permission]:
        """Get permission by resource and action"""
        return self.repository.get_by_resource_and_action(resource, action)

    def get_active_permissions(self) -> List[Permission]:
        """Get all active permissions"""
        return self.repository.get_active_permissions()

    def get_user_permissions(self, user_id: int) -> List[Permission]:
        """Get all permissions for a user"""
        return self.repository.get_user_permissions(user_id)

    def check_permission(self, user_id: int, resource: str, action: str) -> bool:
        """Check if a user has a specific permission"""
        permissions = self.repository.get_user_permissions(user_id)
        for permission in permissions:
            if permission.resource == resource and permission.action == action:
                return True
        return False

    def _check_duplicate_on_create(self, obj_in: PermissionCreate) -> None:
        """Check for duplicate permission"""
        if self.repository.get_by_name(obj_in.name):
            raise DuplicateError(f"Permission with name {obj_in.name} already exists")

    def _check_duplicate_on_update(self, obj_in: PermissionUpdate, id: int) -> None:
        """Check for duplicate permission on update"""
        if hasattr(obj_in, 'name') and obj_in.name:
            existing = self.repository.get_by_name(obj_in.name)
            if existing and existing.id != id:
                raise DuplicateError(f"Permission with name {obj_in.name} already exists")