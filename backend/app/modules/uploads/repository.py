from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.uploads.model import Upload, UploadType
from app.modules.uploads.schemas import UploadCreate, UploadUpdate


class UploadRepository(BaseRepository[Upload, UploadCreate, UploadUpdate]):
    """Repository for Upload model"""

    def __init__(self, db: Session):
        super().__init__(db, Upload)

    def get_by_user(self, user_id: int) -> list[type[Upload]]:
        """Get all uploads by a user"""
        return self.db.query(Upload).filter(
            Upload.user_id == user_id
        ).order_by(Upload.created_at.desc()).all()

    def get_by_type(self, upload_type: UploadType) -> list[type[Upload]]:
        """Get uploads by type"""
        return self.db.query(Upload).filter(
            Upload.upload_type == upload_type,
            Upload.is_public == True
        ).all()

    def get_public_uploads(self) -> list[type[Upload]]:
        """Get all public uploads"""
        return self.db.query(Upload).filter(Upload.is_public == True).all()

    def mark_as_processed(self, upload_id: int) -> Optional[Upload]:
        """Mark an upload as processed"""
        upload = self.get_by_id(upload_id)
        if upload:
            upload.is_processed = True
            self.db.commit()
            self.db.refresh(upload)
        return upload