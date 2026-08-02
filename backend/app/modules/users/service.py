from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.users.repository import UserRepository
from app.modules.users.model import User
from app.modules.users.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import ValidationError, DuplicateError, AuthenticationError, NotFoundError


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for User business logic"""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        super().__init__(self.repository)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = self.repository.get_by_email_or_username(username, username)
        if not user:
            raise AuthenticationError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        if not user.is_active:
            raise AuthenticationError("User account is inactive")

        # Update last login
        self.repository.update_last_login(user.id)

        return user

    def register(self, user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user exists
        if self.repository.get_by_email(user_data.email):
            raise DuplicateError(f"User with email {user_data.email} already exists")

        if self.repository.get_by_username(user_data.username):
            raise DuplicateError(f"User with username {user_data.username} already exists")

        return self.create(user_data)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.repository.get_by_email(email)

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.repository.get_by_username(username)

    def get_profile(self, user_id: int) -> Dict[str, Any]:
        """Get user profile with additional data"""
        user = self.get_by_id(user_id)

        # Get user roles and permissions
        roles = [ur.role.name for ur in user.user_roles]
        permissions = []
        for ur in user.user_roles:
            for rp in ur.role.role_permissions:
                permissions.append(f"{rp.permission.resource}:{rp.permission.action}")

        return {
            "user": user,
            "roles": roles,
            "permissions": list(set(permissions))
        }

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change user password"""
        user = self.get_by_id(user_id)

        if not verify_password(current_password, user.password_hash):
            raise ValidationError("Current password is incorrect")

        # Update password
        hashed_password = get_password_hash(new_password)
        self.repository.update(user_id, {"password_hash": hashed_password})

        return True

    def reset_password(self, email: str, new_password: str) -> bool:
        """Reset user password (for password reset flow)"""
        user = self.repository.get_by_email(email)
        if not user:
            raise NotFoundError(f"User with email {email} not found")

        hashed_password = get_password_hash(new_password)
        self.repository.update(user.id, {"password_hash": hashed_password})

        return True

    def activate_user(self, user_id: int) -> User:
        """Activate a user"""
        user = self.get_by_id(user_id)
        if user.is_active:
            raise ValidationError("User is already active")

        return self.repository.activate_user(user_id)

    def deactivate_user(self, user_id: int) -> User:
        """Deactivate a user"""
        user = self.get_by_id(user_id)
        if not user.is_active:
            raise ValidationError("User is already inactive")

        return self.repository.deactivate_user(user_id)

    def verify_user(self, user_id: int) -> User:
        """Verify a user's email"""
        user = self.get_by_id(user_id)
        if user.is_verified:
            raise ValidationError("User is already verified")

        return self.repository.verify_user(user_id)

    def get_active_users(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[User]:
        """Get active users"""
        return self.repository.get_active_users(skip=skip, limit=limit, search=search)

    # Override validation methods
    def _validate_create(self, obj_in: UserCreate) -> None:
        """Validate user creation"""
        if len(obj_in.password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        if not any(c.isupper() for c in obj_in.password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in obj_in.password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in obj_in.password):
            raise ValidationError("Password must contain at least one number")

    def _check_duplicate_on_create(self, obj_in: UserCreate) -> None:
        """Check for duplicate user"""
        if self.repository.get_by_email(obj_in.email):
            raise DuplicateError(f"User with email {obj_in.email} already exists")

        if self.repository.get_by_username(obj_in.username):
            raise DuplicateError(f"User with username {obj_in.username} already exists")

    def _validate_delete(self, id: int) -> None:
        """Validate user deletion"""
        user = self.get_by_id(id)
        if user.is_superuser:
            raise ValidationError("Cannot delete superuser")