from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the currently authenticated user from the JWT access token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        # Decode and validate JWT
        payload = decode_token(token)

        # Extract token information
        user_id = payload.get("sub")
        token_type = payload.get("type")

        # Validate token type
        if user_id is None or token_type != "access":
            raise credentials_exception

        # Convert user ID from JWT string to integer
        user_id = int(user_id)

    except (ValueError, TypeError):
        raise credentials_exception

    # Find user in database
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    # User does not exist
    if user is None:
        raise credentials_exception

    # User account is inactive
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


def require_role(required_role: str):
    """
    Generic role-based access control dependency.

    Example:
        current_user: User = Depends(require_role("ADMIN"))
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        user_roles = {
            role.name.upper()
            for role in current_user.roles
        }

        if required_role.upper() not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role} role required",
            )

        return current_user

    return role_checker


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow access only to users with ADMIN role.
    """

    return require_role("ADMIN")(current_user)


def require_moderator(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow access only to users with MODERATOR role.
    """

    return require_role("MODERATOR")(current_user)