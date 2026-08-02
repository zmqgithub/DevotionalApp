from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.audit.model import AuditLog
from app.modules.audit.schemas import AuditLogCreate


class AuditRepository(BaseRepository[AuditLog, AuditLogCreate, AuditLogCreate]):
    """Repository for AuditLog model"""

    def __init__(self, db: Session):
        super().__init__(db, AuditLog)

    def log_action(
            self,
            user_id: Optional[int],
            action: str,
            resource_type: str,
            resource_id: Optional[int] = None,
            old_value: Optional[dict] = None,
            new_value: Optional[dict] = None,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None
    ) -> AuditLog:
        """Log an action"""
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_by_user(self, user_id: int, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a user"""
        return self.db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()

    def get_by_resource(self, resource_type: str, resource_id: int) -> List[AuditLog]:
        """Get audit logs for a specific resource"""
        return self.db.query(AuditLog).filter(
            AuditLog.resource_type == resource_type,
            AuditLog.resource_id == resource_id
        ).order_by(AuditLog.created_at.desc()).all()

    def get_by_action(self, action: str, days: int = 7) -> List[AuditLog]:
        """Get audit logs by action type"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return self.db.query(AuditLog).filter(
            AuditLog.action == action,
            AuditLog.created_at >= cutoff
        ).order_by(AuditLog.created_at.desc()).all()