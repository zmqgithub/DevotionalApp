from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    ChangePasswordRequest,
    UserProfileUpdate
)
from app.core.security import hash_password, verify_password
from app.schemas.user import AdminUserUpdate

def get_users(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
):
    query = db.query(User).filter(
        User.is_deleted.is_(False)
    )

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            (User.name.ilike(search_pattern))
            | (User.email.ilike(search_pattern))
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    count_query = query.with_entities(
        func.count(User.id)
    )

    total = db.scalar(count_query) or 0

    total_pages = (
        ceil(total / page_size)
        if total > 0
        else 0
    )

    users = (
        query
        .order_by(User.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return users, total, total_pages

def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:

    return (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

""" def get_user_by_id(
    db: Session,
    user_id: int,
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user """


def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(
            User.email == email,
            User.is_deleted.is_(False),
        )
        .first()
    )


def create_user(
    db: Session,
    data: UserCreate,
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        profile_image_url=data.profile_image_url,
        is_active=True,
        is_deleted=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def update_user(
    db: Session,
    user_id: int,
    user_data,
) -> User:

    # IMPORTANT:
    # user_id must be an integer, never a User object.
    if isinstance(user_id, User):
        user_id = user_id.id

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get only fields actually supplied by the request
    update_data = user_data.model_dump(
        exclude_unset=True,
    )

    # Never allow these fields to be changed through this endpoint
    protected_fields = {
        "id",
        "password_hash",
        "is_deleted",
        "created_at",
        "updated_at",
    }

    for field, value in update_data.items():

        if field in protected_fields:
            continue

        if hasattr(user, field):
            setattr(
                user,
                field,
                value,
            )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

""" def update_user(
    db: Session,
    user_id: int,
    data: UserUpdate,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:
        existing_user = (
            db.query(User)
            .filter(
                User.email == update_data["email"],
                User.id != user_id,
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user """


def change_password(
    db: Session,
    user_id: int,
    data: ChangePasswordRequest,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if not verify_password(
        data.current_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    user.password_hash = hash_password(
        data.new_password
    )

    db.commit()

    return user


def delete_user(
    db: Session,
    user_id: int,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    user.is_deleted = True
    user.is_active = False

    db.commit()

    return user


def restore_user(
    db: Session,
    user_id: int,
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_deleted = False
    user.is_active = True

    db.commit()
    db.refresh(user)

    return user

def soft_delete_user(
    db: Session,
    user_id: int,
) -> User:
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_deleted = True
    user.is_active = False

    db.commit()
    db.refresh(user)

    return user

def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool,
) -> User:
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return user

def admin_update_user(
    db: Session,
    user_id: int,
    data: AdminUserUpdate,
) -> User:
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "password":
            continue

        if hasattr(user, field):
            setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

def update_my_profile(
    db: Session,
    current_user: User,
    data: UserProfileUpdate,
) -> User:
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user