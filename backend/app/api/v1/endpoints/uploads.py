from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.uploads.service import UploadService
from app.modules.uploads.schemas import UploadResponse, UploadType
from app.api.v1.dependencies import get_current_user
from app.modules.users.model import User
from app.schemas.base import MessageResponse

router = APIRouter()


@router.post("/", response_model=UploadResponse)
async def upload_file(
        file: UploadFile = File(...),
        upload_type: UploadType = UploadType.OTHER,
        is_public: bool = True,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Upload a file"""
    service = UploadService(db)

    # Read file content
    content = await file.read()

    return service.save_file(
        file_data=content,
        filename=file.filename,
        user_id=current_user.id,
        upload_type=upload_type
    )


@router.get("/", response_model=List[UploadResponse])
async def get_my_uploads(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get current user's uploads"""
    service = UploadService(db)
    return service.get_by_user(current_user.id)


@router.get("/public", response_model=List[UploadResponse])
async def get_public_uploads(
        db: Session = Depends(get_db)
):
    """Get all public uploads"""
    service = UploadService(db)
    return service.get_public_uploads()


@router.delete("/{upload_id}")
async def delete_upload(
        upload_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete an upload"""
    service = UploadService(db)
    upload = service.get_by_id(upload_id)

    if upload.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this upload"
        )

    service.delete_file(upload_id)
    return MessageResponse(message="File deleted successfully")