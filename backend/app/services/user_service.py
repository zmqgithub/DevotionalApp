from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, ChangePasswordRequest
from app.core.security import hash_password, verify_password


def get_users(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
):
    """
    Get users with pagination, search, and filtering.
    Returns: (users, total_count, total_pages)
    """
    # Build the base query
    query = select(User).where(User.is_deleted.is_(False))
    
    # Apply search filter (search by name or email)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.name.ilike(search_pattern)) | 
            (User.email.ilike(search_pattern))
        )
    
    # Apply is_active filter
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(query.subquery())
    total = db.scalar(count_query)
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # Execute query
    users = db.scalars(query).all()
    
    return users, total, total_pages


def get_user_by_id(
    db: Session,
    user_id: int,
):
    statement = select(User).where(
        User.id == user_id,
        User.is_deleted.is_(False),
    )
    return db.scalar(statement)


def get_user_by_email(
    db: Session,
    email: str,
):
    statement = select(User).where(
        User.email == email,
        User.is_deleted.is_(False),
    )
    return db.scalar(statement)


def create_user(
    db: Session,
    user_data: UserCreate,
):
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        profile_image_url=user_data.profile_image_url,
        is_active=True,
        is_deleted=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session,
    user: User,
    user_data: UserUpdate,
):
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.profile_image_url is not None:
        user.profile_image_url = user_data.profile_image_url
    if user_data.password is not None:
        user.password_hash = hash_password(user_data.password)
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(
    db: Session,
    user: User,
):
    user.is_deleted = True
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def change_password(
    db: Session,
    user: User,
    password_data: ChangePasswordRequest,
):
    """
    Change user's password with validation.
    """
    # Verify current password
    if not verify_password(password_data.current_password, user.password_hash):
        raise ValueError("Current password is incorrect")
    
    # Validate new password
    if len(password_data.new_password) < 8:
        raise ValueError("New password must be at least 8 characters long")
    
    # Update password
    user.password_hash = hash_password(password_data.new_password)
    
    db.commit()
    db.refresh(user)
    return user


def update_user_status(
    db: Session,
    user: User,
    is_active: bool,
):
    """
    Update user's active status.
    """
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(
    db: Session,
    user: User,
):
    """
    Soft delete a user (mark as deleted but keep in database).
    """
    user.is_deleted = True
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user