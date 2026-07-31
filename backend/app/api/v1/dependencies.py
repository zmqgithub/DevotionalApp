from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


# ============================================================
# GET CURRENT AUTHENTICATED USER
# ============================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the currently authenticated user from JWT access token.

    Any authenticated active user can pass this dependency.

    Roles:
    - ADMIN
    - MODERATOR
    - USER
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

        # Token must contain user ID
        if user_id is None:
            raise credentials_exception

        # Only access tokens are accepted
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

    # Inactive users cannot access protected APIs
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


# ============================================================
# GET CURRENT USER ROLES
# ============================================================

def get_user_roles(
    current_user: User = Depends(get_current_user),
) -> set[str]:
    """
    Return all roles assigned to the current user.

    Example:
        {"ADMIN"}
        {"MODERATOR"}
        {"USER"}

    The role names are normalized to uppercase.
    """

    return {
        role.name.upper()
        for role in current_user.roles
    }


# ============================================================
# GENERIC ROLE CHECKER
# ============================================================

def require_any_role(*allowed_roles: str):
    """
    Allow access when the current user has at least one
    of the specified roles.

    Example:

        Depends(require_any_role("ADMIN", "MODERATOR"))

    Allows:
        ADMIN
        MODERATOR

    Blocks:
        USER
    """

    normalized_roles = {
        role.upper()
        for role in allowed_roles
    }

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        user_roles = {
            role.name.upper()
            for role in current_user.roles
        }

        if not user_roles.intersection(normalized_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker


# ============================================================
# ADMIN ONLY
# ============================================================

def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    ADMIN ONLY.

    Permission hierarchy:

        ADMIN
          ├── Admin APIs
          ├── Moderator APIs
          ├── User APIs
          └── Own Profile APIs

    Only users with ADMIN role can pass this dependency.
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


# ============================================================
# ADMIN + MODERATOR
# ============================================================

def require_moderator(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    ADMIN + MODERATOR.

    Permission hierarchy:

        ADMIN
          └── Moderator APIs

        MODERATOR
          └── Moderator APIs

    ADMIN also has access because ADMIN inherits
    all lower-level permissions.
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


# ============================================================
# ANY AUTHENTICATED USER
# ============================================================

def require_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Any authenticated active user.

    Allows:
        ADMIN
        MODERATOR
        USER

    Permission hierarchy:

        ADMIN
          └── User APIs

        MODERATOR
          └── User APIs

        USER
          └── User APIs
    """

    return current_user


# ============================================================
# EXACT ROLE CHECKER
# ============================================================

def require_role(required_role: str):
    """
    Require an exact role.

    This does NOT implement role hierarchy.

    Example:

        Depends(require_role("ADMIN"))

    Allows:
        ADMIN

    Blocks:
        MODERATOR
        USER
    """

    normalized_required_role = required_role.upper()

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        user_roles = {
            role.name.upper()
            for role in current_user.roles
        }

        if normalized_required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"{normalized_required_role} role required"
                ),
            )

        return current_user

    return role_checker