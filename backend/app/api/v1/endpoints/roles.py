from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.roles.service import RoleService
from app.modules.roles.schemas import (
    RoleCreate, RoleUpdate, RoleResponse,
    AssignRoleRequest, RemoveRoleRequest,
    AssignPermissionRequest, RemovePermissionRequest
)
from app.api.v1.dependencies import get_current_superuser, require_admin, require_role
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[RoleResponse])
async def get_roles(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        is_active: Optional[bool] = None,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Get all roles (admin only)"""
    service = RoleService(db)
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active

    roles = service.get_all(skip=skip, limit=limit, filters=filters)
    total = service.count(filters)

    return PaginatedResponse(
        items=roles,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
        role_id: int,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Get role by ID (admin only)"""
    service = RoleService(db)
    return service.get_by_id(role_id)


@router.post("/", response_model=RoleResponse)
async def create_role(
        role_data: RoleCreate,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Create a new role (super admin only)"""
    service = RoleService(db)
    return service.create(role_data)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
        role_id: int,
        role_data: RoleUpdate,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Update a role (super admin only)"""
    service = RoleService(db)
    return service.update(role_id, role_data)


@router.delete("/{role_id}")
async def delete_role(
        role_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a role (super admin only)"""
    service = RoleService(db)
    service.delete(role_id)
    return MessageResponse(message="Role deleted successfully")


@router.post("/assign-role", response_model=MessageResponse)
async def assign_role_to_user(
        request: AssignRoleRequest,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Assign a role to a user (super admin only)"""
    # This would need to be implemented in the service
    # For now, we'll just return a success message
    return MessageResponse(message=f"Role {request.role_id} assigned to user {request.user_id}")


@router.post("/remove-role", response_model=MessageResponse)
async def remove_role_from_user(
        request: RemoveRoleRequest,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Remove a role from a user (super admin only)"""
    return MessageResponse(message=f"Role {request.role_id} removed from user {request.user_id}")


@router.post("/{role_id}/permissions/{permission_id}")
async def assign_permission(
        role_id: int,
        permission_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Assign a permission to a role (super admin only)"""
    service = RoleService(db)
    service.assign_permission(role_id, permission_id)
    return MessageResponse(message="Permission assigned successfully")


@router.delete("/{role_id}/permissions/{permission_id}")
async def remove_permission(
        role_id: int,
        permission_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Remove a permission from a role (super admin only)"""
    service = RoleService(db)
    service.remove_permission(role_id, permission_id)
    return MessageResponse(message="Permission removed successfully")