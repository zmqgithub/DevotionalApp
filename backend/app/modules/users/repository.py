from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.repositories.base import BaseRepository
from app.modules.users.model import User
from app.modules.users.schemas import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository for User model"""

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email_or_username(self, email: str, username: str) -> Optional[User]:
        """Get user by email or username"""
        return self.db.query(User).filter(
            or_(User.email == email, User.username == username)
        ).first()

    def get_active_users(
            self,
            skip: int = 0,
            limit: int = 100,
            search: Optional[str] = None
    ) -> List[User]:
        """Get active users with optional search"""
        query = self.db.query(User).filter(User.is_active == True)

        if search:
            query = query.filter(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%")
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_users_by_role(self, role_name: str) -> List[User]:
        """Get users by role name"""
        return self.db.query(User).join(User.user_roles).join(User.user_roles.role).filter(
            User.roles.name == role_name
        ).all()

    def update_last_login(self, user_id: int) -> Optional[User]:
        """Update user's last login timestamp"""
        user = self.get_by_id(user_id)
        if user:
            from datetime import datetime
            user.last_login = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
        return user

    def activate_user(self, user_id: int) -> Optional[User]:
        """Activate a user account"""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = True
            user.status = "active"
            self.db.commit()
            self.db.refresh(user)
        return user

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user account"""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            user.status = "inactive"
            self.db.commit()
            self.db.refresh(user)
        return user

    def verify_user(self, user_id: int) -> Optional[User]:
        """Verify a user's email"""
        user = self.get_by_id(user_id)
        if user:
            user.is_verified = True
            self.db.commit()
            self.db.refresh(user)
        return user