from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import (
    get_current_user,
    require_role,
)
from app.core.database import get_db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole

from app.schemas.role import (
    AssignRoleRequest,
    RoleResponse,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(require_role("ADMIN")),
):
    return {
        "message": "Welcome Admin",
        "email": current_user.email,
    }


@router.get(
    "/roles",
    response_model=list[RoleResponse],
)
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN")),
):

    return (
        db.query(Role)
        .order_by(Role.name)
        .all()
    )


@router.post(
    "/users/{user_id}/roles",
    response_model=RoleResponse,
)
def assign_role(
    user_id: int,
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN")),
):
    # Make sure path user_id and body user_id match
    if user_id != request.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID in path and request body must match",
        )

    # Check target user
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

    # Check role
    role = (
        db.query(Role)
        .filter(Role.id == request.role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    # Check duplicate assignment
    existing_user_role = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_id,
            UserRole.role_id == request.role_id,
        )
        .first()
    )

    if existing_user_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User already has the {role.name} role",
        )

    # Assign role
    user_role = UserRole(
        user_id=user_id,
        role_id=role.id,
    )

    db.add(user_role)
    db.commit()

    return role


@router.delete(
    "/users/{user_id}/roles/{role_name}",
)
def remove_role(
    user_id: int,
    role_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN")),
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = (
        db.query(Role)
        .filter(
            Role.name == role_name.upper()
        )
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    user_role = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user.id,
            UserRole.role_id == role.id,
        )
        .first()
    )

    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have this role",
        )

    db.delete(user_role)
    db.commit()

    return {
        "message": "Role removed successfully",
        "user_id": user.id,
        "role": role.name,
    }