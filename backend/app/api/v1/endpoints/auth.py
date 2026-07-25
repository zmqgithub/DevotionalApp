from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse


from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    AccessTokenResponse,
)

from app.services.auth_service import (
    login_user,
    refresh_access_token,
)

from app.core.database import get_db

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db,
        login_data.email,
        login_data.password,
    )


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
):
    return refresh_access_token(
        request.refresh_token
    )

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user