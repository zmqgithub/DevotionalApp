from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.users.service import UserService
from app.modules.users.model import User
from app.modules.permissions.service import PermissionService
from app.core.security import verify_access_token
from app.core.exceptions import AuthenticationError

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials

    # Verify token
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service = UserService(db)
    user = user_service.get_by_id(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return current_user


async def get_current_superuser(
        current_user: User = Depends(get_current_user)
) -> User:
    """Get current superuser"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required"
        )
    return current_user


async def require_admin(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> User:
    """Require admin role"""
    # Check if user has admin role
    user_roles = [ur.role.name for ur in current_user.user_roles]

    if "admin" not in user_roles and "super_admin" not in user_roles and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return current_user


async def require_role(role_name: str):
    """Create a dependency that requires a specific role"""

    async def role_dependency(
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db)
    ) -> User:
        user_roles = [ur.role.name for ur in current_user.user_roles]

        if role_name not in user_roles and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role_name}' required"
            )

        return current_user

    return role_dependency


async def require_permission(
        resource: str,
        action: str
):
    """Create a dependency that requires a specific permission"""

    async def permission_dependency(
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db)
    ) -> User:
        permission_service = PermissionService(db)
        has_permission = permission_service.check_permission(
            current_user.id, resource, action
        )

        if not has_permission and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {resource}:{action}"
            )

        return current_user

    return permission_dependency


def get_current_user_optional(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
        db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise None"""
    if not credentials:
        return None

    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None