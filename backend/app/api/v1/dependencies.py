from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

def require_any_role(*allowed_roles: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        user_roles = {
            role.name.upper()
            for role in current_user.roles
        }

        if not user_roles.intersection(
            {role.upper() for role in allowed_roles}
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the currently authenticated user from JWT access token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = decode_token(token)

        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None:
            raise credentials_exception

        if token_type != "access":
            raise credentials_exception

        user_id = int(user_id)

    except (ValueError, TypeError):
        raise credentials_exception

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


def get_user_roles(
    current_user: User = Depends(get_current_user),
) -> set[str]:
    """
    Return all roles assigned to the current user.
    """

    return {
        role.name.upper()
        for role in current_user.roles
    }


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    ADMIN only.

    Access:
    - Admin APIs
    - Moderator APIs
    - User APIs
    - Own Profile APIs
    """

    user_roles = {
        role.name.upper()
        for role in current_user.roles
    }

    if "ADMIN" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_moderator(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    ADMIN or MODERATOR.

    Access:
    - Moderator APIs
    - User APIs
    - Own Profile APIs
    """

    user_roles = {
        role.name.upper()
        for role in current_user.roles
    }

    if not (
        "ADMIN" in user_roles
        or "MODERATOR" in user_roles
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator access required",
        )

    return current_user


def require_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Any authenticated user.

    Access:
    - User APIs
    - Own Profile APIs

    ADMIN and MODERATOR also pass this check.
    """

    return current_user


def require_role(required_role: str):
    """
    Generic exact role checker.

    Use this when an endpoint requires
    a specific role only.
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
                detail=f"{required_role.upper()} role required",
            )

        return current_user

    return role_checker