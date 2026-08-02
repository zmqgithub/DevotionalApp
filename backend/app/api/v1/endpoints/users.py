from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.users.service import UserService
from app.modules.users.schemas import (
    UserCreate, UserUpdate, UserResponse, UserProfileResponse
)
from app.api.v1.dependencies import get_current_user, get_current_superuser
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
        current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update current user profile"""
    service = UserService(db)
    return service.update(current_user.id, user_update)


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def get_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        search: Optional[str] = None,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    service = UserService(db)
    users = service.get_active_users(skip=skip, limit=limit, search=search)
    total = service.count()

    return PaginatedResponse(
        items=users,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Get user by ID (admin only)"""
    service = UserService(db)
    return service.get_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: int,
        user_update: UserUpdate,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Update user (admin only)"""
    service = UserService(db)
    return service.update(user_id, user_update)


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
        user_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    service = UserService(db)
    service.delete(user_id)
    return MessageResponse(message="User deleted successfully")


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
        user_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Activate user (admin only)"""
    service = UserService(db)
    return service.activate_user(user_id)


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
        user_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Deactivate user (admin only)"""
    service = UserService(db)
    return service.deactivate_user(user_id)


@router.post("/{user_id}/verify", response_model=UserResponse)
async def verify_user(
        user_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Verify user email (admin only)"""
    service = UserService(db)
    return service.verify_user(user_id)