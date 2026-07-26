from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    ChangePasswordRequest,
    UserCreate,
    UserListResponse,
    UserResponse,
    UserStatusUpdate,
    UserUpdate,
    AdminUserUpdate,
    UserProfileUpdate,
)
from app.services.user_service import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    soft_delete_user,
    update_user,
    update_user_status,
    admin_update_user,
    update_my_profile,
    change_password,

)

from app.api.v1.dependencies import (
    get_current_user,
    require_admin,
)
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

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
):

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


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db),
):

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


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_existing_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):

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
        db,
        user,
        user_data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    delete_user(
        db,
        user,
    )

    return None

@router.put(
    "/{user_id}/password",
)
def change_user_password(
    user_id: int,
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
):

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:

        raise HTTPException(
            status_code=404,
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
            status_code=400,
            detail=str(error),
        )

    return {
        "message": "Password changed successfully"
    }

@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def change_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db),
):

    user = get_user_by_id(
        db,
        user_id,
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return update_user_status(
        db,
        user,
        status_data.is_active,
    )

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.put(
    "/me",
    response_model=UserResponse,
)
def update_my_profile_endpoint(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_my_profile(
        db,
        current_user,
        data,
    )

@router.get(
    "",
)
def list_users(
    page: int = Query(
        1,
        ge=1,
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
    ),
    search: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    users, total, total_pages = get_users(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        is_active=is_active,
    )

    return {
        "data": users,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_user_by_id(
        db,
        user_id,
    )

@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def change_user_status(
    user_id: int,
    data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = get_user_by_id(
        db,
        user_id,
    )

    return update_user_status(
        db,
        user,
        data.is_active,
    )

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = get_user_by_id(
        db,
        user_id,
    )

    soft_delete_user(
        db,
        user,
    )

    return None

