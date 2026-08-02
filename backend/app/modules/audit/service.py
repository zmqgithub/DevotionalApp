from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.audit.repository import AuditRepository
from app.modules.audit.model import AuditLog
from app.modules.audit.schemas import AuditLogCreate
from app.core.exceptions import NotFoundError


class AuditService(BaseService[AuditLog, AuditLogCreate, AuditLogCreate]):
    """Service for Audit business logic"""

    def __init__(self, db: Session):
        self.repository = AuditRepository(db)
        super().__init__(self.repository)

    def log_action(
            self,
            user_id: Optional[int],
            action: str,
            resource_type: str,
            resource_id: Optional[int] = None,
            old_value: Optional[Dict[str, Any]] = None,
            new_value: Optional[Dict[str, Any]] = None,
            ip_address: Optional[str] = None,
            user_agent: Optional[str] = None
    ) -> AuditLog:
        """Log an action"""
        return self.repository.log_action(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent
        )

    def get_by_user(self, user_id: int, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a user"""
        if limit <= 0 or limit > 1000:
            raise ValidationError("Limit must be between 1 and 1000")
        return self.repository.get_by_user(user_id, limit)

    def get_by_resource(self, resource_type: str, resource_id: int) -> List[AuditLog]:
        """Get audit logs for a specific resource"""
        return self.repository.get_by_resource(resource_type, resource_id)

    def get_by_action(self, action: str, days: int = 7) -> List[AuditLog]:
        """Get audit logs by action type"""
        if days <= 0:
            raise ValidationError("Days must be greater than 0")
        return self.repository.get_by_action(action, days)

    def get_recent_activities(self, limit: int = 50) -> List[AuditLog]:
        """Get recent activities"""
        if limit <= 0 or limit > 1000:
            raise ValidationError("Limit must be between 1 and 1000")
        return self.repository.get_all(limit=limit, order_by='created_at', order_desc=True)

    def get_user_activity_summary(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get activity summary for a user"""
        logs = self.repository.get_by_user(user_id, limit=1000)

        # Filter by date
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_logs = [log for log in logs if log.created_at >= cutoff]

        # Count actions
        action_counts = {}
        for log in recent_logs:
            action_counts[log.action] = action_counts.get(log.action, 0) + 1

        return {
            'total_actions': len(recent_logs),
            'unique_days': len(set(log.created_at.date() for log in recent_logs)),
            'most_common_action': max(action_counts.items(), key=lambda x: x[1])[0] if action_counts else None,
            'action_breakdown': action_counts
        }