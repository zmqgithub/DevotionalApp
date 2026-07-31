from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User

from app.schemas.role import (
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)

from app.services.role_service import (
    get_roles,
    get_role,
    create_role,
    update_role,
    delete_role,
    assign_role_to_user,
    remove_role_from_user,
)


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


# ============================================================
# GET ALL ROLES
# ============================================================

@router.get(
    "",
    response_model=list[RoleResponse],
)
def list_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_roles(db)


# ============================================================
# GET ROLE BY ID
# ============================================================

@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role_by_id(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_role(
        db,
        role_id,
    )


# ============================================================
# CREATE ROLE
# ============================================================

@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return create_role(
        db,
        data,
    )


# ============================================================
# UPDATE ROLE
# ============================================================

@router.put(
    "/{role_id}",
    response_model=RoleResponse,
)
def update_existing_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return update_role(
        db,
        role_id,
        data,
    )


# ============================================================
# DELETE ROLE
# ============================================================

@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    delete_role(
        db,
        role_id,
    )

    return None
