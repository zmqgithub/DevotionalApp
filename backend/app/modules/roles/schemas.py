from __future__ import annotations
from pydantic import Field
from typing import Optional, List
from app.schemas.base import BaseSchema, TimestampSchema

class RoleBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class RoleResponse(RoleBase, TimestampSchema):
    id: int
    is_active: bool
    is_system: bool

class RoleWithPermissionsResponse(RoleResponse):
    permissions: List[int] = []  # List of permission IDs

class AssignRoleRequest(BaseSchema):
    """Request to assign a role to a user"""
    user_id: int
    role_id: int

class RemoveRoleRequest(BaseSchema):
    """Request to remove a role from a user"""
    user_id: int
    role_id: int

class AssignPermissionRequest(BaseSchema):
    """Request to assign a permission to a role"""
    permission_id: int

class RemovePermissionRequest(BaseSchema):
    """Request to remove a permission from a role"""
    permission_id: int