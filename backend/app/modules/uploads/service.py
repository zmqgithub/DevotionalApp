from typing import Optional, List
import os
import shutil
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.uploads.repository import UploadRepository
from app.modules.uploads.model import Upload, UploadType
from app.modules.uploads.schemas import UploadCreate, UploadUpdate
from app.core.exceptions import ValidationError, NotFoundError
from app.core.config import settings


class UploadService(BaseService[Upload, UploadCreate, UploadUpdate]):
    """Service for Upload business logic"""

    def __init__(self, db: Session):
        self.repository = UploadRepository(db)
        super().__init__(self.repository)
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)

    def get_by_user(self, user_id: int) -> List[Upload]:
        """Get all uploads by a user"""
        return self.repository.get_by_user(user_id)

    def get_by_type(self, upload_type: UploadType) -> List[Upload]:
        """Get uploads by type"""
        return self.repository.get_by_type(upload_type)

    def get_public_uploads(self) -> List[Upload]:
        """Get all public uploads"""
        return self.repository.get_public_uploads()

    def save_file(self, file_data: bytes, filename: str, user_id: int, upload_type: UploadType) -> Upload:
        """Save a file and create upload record"""
        # Validate file size
        if len(file_data) > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE} bytes")

        # Generate safe filename
        safe_filename = self._get_safe_filename(filename)
        file_path = self.upload_dir / safe_filename

        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Create upload record
        upload_data = {
            'file_name': filename,
            'file_path': str(file_path),
            'file_url': f"/uploads/{safe_filename}",
            'file_size': len(file_data),
            'mime_type': self._get_mime_type(filename),
            'upload_type': upload_type,
            'user_id': user_id,
            'is_public': True
        }

        upload = Upload(**upload_data)
        self.repository.db.add(upload)
        self.repository.db.commit()
        self.repository.db.refresh(upload)
        return upload

    def delete_file(self, upload_id: int) -> bool:
        """Delete a file and its record"""
        upload = self.get_by_id(upload_id)

        # Delete physical file
        file_path = Path(upload.file_path)
        if file_path.exists():
            file_path.unlink()

        return self.repository.delete(upload_id)

    def mark_as_processed(self, upload_id: int) -> Upload:
        """Mark an upload as processed"""
        upload = self.get_by_id(upload_id)
        if upload.is_processed:
            raise ValidationError("Upload is already processed")

        return self.repository.mark_as_processed(upload_id)

    def _get_safe_filename(self, filename: str) -> str:
        """Generate a safe filename"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        return f"{timestamp}_{name}{ext}"

    def _get_mime_type(self, filename: str) -> str:
        """Get MIME type from filename"""
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.mp4': 'video/mp4',
            '.mp3': 'audio/mpeg',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        return mime_types.get(ext, 'application/octet-stream')