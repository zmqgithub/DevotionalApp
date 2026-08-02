from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.audit.service import AuditService
from app.modules.audit.schemas import AuditLogResponse
from app.api.v1.dependencies import get_current_superuser
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[AuditLogResponse])
async def get_audit_logs(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Get audit logs (super admin only)"""
    service = AuditService(db)

    filters = {}
    if user_id:
        filters['user_id'] = user_id
    if action:
        filters['action'] = action
    if resource_type:
        filters['resource_type'] = resource_type

    logs = service.get_all(skip=skip, limit=limit, filters=filters, order_by='created_at', order_desc=True)
    total = service.count(filters)

    return PaginatedResponse(
        items=logs,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/user/{user_id}", response_model=List[AuditLogResponse])
async def get_user_audit_logs(
        user_id: int,
        limit: int = Query(100, ge=1, le=1000),
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Get audit logs for a specific user (super admin only)"""
    service = AuditService(db)
    return service.get_by_user(user_id, limit)


@router.get("/resource/{resource_type}/{resource_id}", response_model=List[AuditLogResponse])
async def get_resource_audit_logs(
        resource_type: str,
        resource_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Get audit logs for a specific resource (super admin only)"""
    service = AuditService(db)
    return service.get_by_resource(resource_type, resource_id)


@router.get("/summary/user/{user_id}")
async def get_user_activity_summary(
        user_id: int,
        days: int = Query(30, ge=1, le=365),
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Get user activity summary (super admin only)"""
    service = AuditService(db)
    return service.get_user_activity_summary(user_id, days)