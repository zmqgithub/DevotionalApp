from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    auth,
    users,
    admin,
    roles,
)

api_router = APIRouter()

api_router.include_router(
    health.router
)

api_router.include_router(
    users.router
)

api_router.include_router(
    auth.router
)

api_router.include_router(
    admin.router
)

api_router.include_router(
    roles.router
)