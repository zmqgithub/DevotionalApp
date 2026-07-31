from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

from app.schemas.user import (
    ChangePasswordRequest,
    UserCreate,
    UserListResponse,
    UserResponse,
    UserStatusUpdate,
    UserUpdate,
    UserProfileUpdate,
)

from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    update_user,
    update_user_status,
    update_my_profile,
    change_password,
    soft_delete_user,
)

from app.api.v1.dependencies import (
    get_current_user,
    require_admin,
    require_any_role,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ============================================================
# CREATE USER
# ADMIN ONLY
# ============================================================

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Create a new user.

    Permission:
        ADMIN only
    """

    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    return create_user(
        db,
        user_data,
    )


# ============================================================
# GET MY PROFILE
# ADMIN + MODERATOR + USER
# ============================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get the currently authenticated user's own profile.

    Permission:
        ADMIN
        MODERATOR
        USER
    """

    return current_user


# ============================================================
# UPDATE MY PROFILE
# ADMIN + MODERATOR + USER
# ============================================================

@router.put(
    "/me",
    response_model=UserResponse,
)
def update_my_profile_endpoint(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the currently authenticated user's own profile.

    Permission:
        ADMIN
        MODERATOR
        USER
    """

    return update_my_profile(
        db,
        current_user,
        data,
    )


# ============================================================
# LIST USERS
# ADMIN + MODERATOR
# ============================================================

@router.get(
    "",
    response_model=UserListResponse,
)
def get_all_users(
    page: int = Query(
        1,
        ge=1,
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        None,
        description="Search by name or email",
    ),
    is_active: bool | None = Query(
        None,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "ADMIN",
            "MODERATOR",
        )
    ),
):
    """
    List all users.

    Permission:
        ADMIN
        MODERATOR
    """

    users, total, total_pages = get_users(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        is_active=is_active,
    )

    return UserListResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# ============================================================
# GET SINGLE USER
# ADMIN + MODERATOR
# ============================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "ADMIN",
            "MODERATOR",
        )
    ),
):
    """
    Get a specific user by ID.

    Permission:
        ADMIN
        MODERATOR
    """

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# ============================================================
# UPDATE USER
# ADMIN ONLY
# ============================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Update another user's account.

    Permission:
        ADMIN only
    """

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_data.email:

        existing_user = get_user_by_email(
            db,
            user_data.email,
        )

        if (
            existing_user
            and existing_user.id != user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already used by another user",
            )

    return update_user(
        db=db,
        user_id=user_id,
        user_data=user_data,
    )


# ============================================================
# DELETE USER
# ADMIN ONLY
# ============================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Soft delete a user.

    Permission:
        ADMIN only
    """

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    soft_delete_user(
        db,
        user,
    )

    return None


# ============================================================
# CHANGE USER PASSWORD
# ADMIN ONLY
# ============================================================

@router.put(
    "/{user_id}/password",
)
def change_user_password(
    user_id: int,
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Change another user's password.

    Permission:
        ADMIN only
    """

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        change_password(
            db,
            user,
            password_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    return {
        "message": "Password changed successfully",
    }


# ============================================================
# CHANGE USER STATUS
# ADMIN ONLY
# ============================================================

@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def change_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Activate or deactivate a user.

    Permission:
        ADMIN only
    """

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return update_user_status(
        db,
        user,
        status_data.is_active,
    )