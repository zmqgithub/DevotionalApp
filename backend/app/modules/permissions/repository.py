from typing import Optional, List
from sqlalchemy.orm import Session

from app.modules import Role, User
from app.repositories.base import BaseRepository
from app.modules.permissions.model import Permission
from app.modules.permissions.schemas import PermissionCreate, PermissionUpdate


class PermissionRepository(BaseRepository[Permission, PermissionCreate, PermissionUpdate]):
    """Repository for Permission model"""

    def __init__(self, db: Session):
        super().__init__(db, Permission)

    def get_by_name(self, name: str) -> Optional[Permission]:
        """Get permission by name"""
        return self.db.query(Permission).filter(Permission.name == name).first()

    def get_by_resource(self, resource: str) -> List[Permission]:
        """Get permissions by resource"""
        return self.db.query(Permission).filter(Permission.resource == resource).all()

    def get_by_action(self, action: str) -> List[Permission]:
        """Get permissions by action"""
        return self.db.query(Permission).filter(Permission.action == action).all()

    def get_by_resource_and_action(self, resource: str, action: str) -> Optional[Permission]:
        """Get permission by resource and action"""
        return self.db.query(Permission).filter(
            Permission.resource == resource,
            Permission.action == action
        ).first()

    def get_active_permissions(self) -> List[Permission]:
        """Get all active permissions"""
        return self.db.query(Permission).filter(Permission.is_active == True).all()

    def get_user_permissions(self, user_id: int) -> List[Permission]:
        """Get all permissions for a user"""
        return self.db.query(Permission).join(
            Permission.role_permissions
        ).join(
            Permission.role_permissions.role
        ).join(
            Role.user_roles
        ).filter(
            User.id == user_id,
            Permission.is_active == True
        ).distinct().all()