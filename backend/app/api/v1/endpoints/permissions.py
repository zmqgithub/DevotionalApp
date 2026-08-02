# app/api/v1/endpoints/permissions.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.permissions.service import PermissionService
from app.modules.permissions.schemas import (
    PermissionCreate, PermissionUpdate, PermissionResponse
)
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[PermissionResponse])
async def get_permissions(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        resource: Optional[str] = None,
        action: Optional[str] = None,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Get all permissions (admin only)"""
    service = PermissionService(db)

    if resource and action:
        permissions = service.get_by_resource_and_action(resource, action)
        return PaginatedResponse(
            items=[permissions] if permissions else [],
            total=1 if permissions else 0,
            page=1,
            size=limit,
            pages=1
        )

    filters = {}
    if resource:
        filters['resource'] = resource
    if action:
        filters['action'] = action

    permissions = service.get_all(skip=skip, limit=limit, filters=filters)
    total = service.count(filters)

    return PaginatedResponse(
        items=permissions,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
        permission_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Get permission by ID (admin only)"""
    service = PermissionService(db)
    return service.get_by_id(permission_id)


@router.post("/", response_model=PermissionResponse)
async def create_permission(
        permission_data: PermissionCreate,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Create a new permission (super admin only)"""
    service = PermissionService(db)
    return service.create(permission_data)


@router.put("/{permission_id}", response_model=PermissionResponse)
async def update_permission(
        permission_id: int,
        permission_data: PermissionUpdate,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Update a permission (super admin only)"""
    service = PermissionService(db)
    return service.update(permission_id, permission_data)


@router.delete("/{permission_id}")
async def delete_permission(
        permission_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a permission (super admin only)"""
    service = PermissionService(db)
    service.delete(permission_id)
    return MessageResponse(message="Permission deleted successfully")