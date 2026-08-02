# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.users.service import UserService
from app.modules.users.schemas import UserCreate, UserResponse
from app.schemas.auth import (
    LoginRequest, RegisterRequest, TokenResponse,
    RefreshTokenRequest, ChangePasswordRequest
)
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.api.v1.dependencies import get_current_user
from app.modules.users.model import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
        login_data: LoginRequest,
        db: Session = Depends(get_db)
):
    """Login user"""
    service = UserService(db)
    user = service.authenticate(login_data.username, login_data.password)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600  # 1 hour
    )


@router.post("/register", response_model=UserResponse)
async def register(
        register_data: RegisterRequest,
        db: Session = Depends(get_db)
):
    """Register new user"""
    service = UserService(db)
    user_data = UserCreate(
        email=register_data.email,
        username=register_data.username,
        full_name=register_data.full_name,
        password=register_data.password
    )
    return service.register(user_data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        refresh_data: RefreshTokenRequest,
        db: Session = Depends(get_db)
):
    """Refresh access token"""
    payload = verify_refresh_token(refresh_data.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    service = UserService(db)
    user = service.get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600
    )


@router.post("/logout")
async def logout(
        current_user: User = Depends(get_current_user)
):
    """Logout user"""
    return {"message": "Logged out successfully"}


@router.post("/change-password")
async def change_password(
        password_data: ChangePasswordRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Change user password"""
    service = UserService(db)
    service.change_password(
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )
    return {"message": "Password changed successfully"}