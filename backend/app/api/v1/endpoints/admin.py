from fastapi import APIRouter, Depends

from app.api.v1.dependencies import require_admin
from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Welcome Admin",
        "email": current_user.email,
    }