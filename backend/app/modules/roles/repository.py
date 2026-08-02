from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.roles.model import Role
from app.modules.roles.schemas import RoleCreate, RoleUpdate


class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    """Repository for Role model"""

    def __init__(self, db: Session):
        super().__init__(db, Role)

    def get_by_name(self, name: str) -> Optional[Role]:
        """Get role by name"""
        return self.db.query(Role).filter(Role.name == name).first()

    def get_active_roles(self) -> List[Role]:
        """Get all active roles"""
        return self.db.query(Role).filter(Role.is_active == True).all()

    def get_system_roles(self) -> List[Role]:
        """Get all system roles"""
        return self.db.query(Role).filter(Role.is_system == True).all()

    def get_role_with_permissions(self, role_id: int) -> Optional[Role]:
        """Get role with its permissions"""
        return self.db.query(Role).filter(Role.id == role_id).first()

    def assign_permission(self, role_id: int, permission_id: int) -> bool:
        """Assign a permission to a role"""
        role = self.get_by_id(role_id)
        if not role:
            return False

        from app.modules.permissions.model import Permission
        permission = self.db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            return False

        if permission not in role.permissions:
            role.permissions.append(permission)
            self.db.commit()
        return True

    def remove_permission(self, role_id: int, permission_id: int) -> bool:
        """Remove a permission from a role"""
        role = self.get_by_id(role_id)
        if not role:
            return False

        from app.modules.permissions.model import Permission
        permission = self.db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            return False

        if permission in role.permissions:
            role.permissions.remove(permission)
            self.db.commit()
        return True