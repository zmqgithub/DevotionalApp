from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.comments.repository import CommentRepository
from app.modules.comments.model import Comment
from app.modules.comments.schemas import CommentCreate, CommentUpdate
from app.core.exceptions import ValidationError, NotFoundError


class CommentService(BaseService[Comment, CommentCreate, CommentUpdate]):
    """Service for Comment business logic"""

    def __init__(self, db: Session):
        self.repository = CommentRepository(db)
        super().__init__(self.repository)

    def get_by_content(self, content_id: int) -> List[Comment]:
        """Get all comments for a content item"""
        return self.repository.get_by_content(content_id)

    def get_by_user(self, user_id: int) -> List[Comment]:
        """Get all comments by a user"""
        return self.repository.get_by_user(user_id)

    def get_replies(self, comment_id: int) -> List[Comment]:
        """Get all replies to a comment"""
        comment = self.get_by_id(comment_id)
        return self.repository.get_replies(comment_id)

    def create_comment(self, user_id: int, content_id: int, text: str) -> Comment:
        """Create a new comment"""
        # Check if content exists and allows comments
        from app.modules.contents.service import ContentService
        content_service = ContentService(self.repository.db)
        content = content_service.get_by_id(content_id)

        if not content.allow_comments:
            raise ValidationError("Comments are disabled for this content")

        comment_data = CommentCreate(
            content=text,
            content_id=content_id,
            user_id=user_id
        )

        return self.create(comment_data)

    def reply_to_comment(self, user_id: int, parent_id: int, text: str) -> Comment:
        """Reply to a comment"""
        parent = self.get_by_id(parent_id)
        if not parent.is_approved:
            raise ValidationError("Cannot reply to unapproved comment")

        comment_data = CommentCreate(
            content=text,
            content_id=parent.content_id,
            user_id=user_id,
            parent_id=parent_id
        )

        return self.create(comment_data)

    def approve_comment(self, comment_id: int) -> Comment:
        """Approve a comment"""
        comment = self.get_by_id(comment_id)
        if comment.is_approved:
            raise ValidationError("Comment is already approved")

        return self.repository.approve_comment(comment_id)

    def pin_comment(self, comment_id: int) -> Comment:
        """Pin a comment"""
        comment = self.get_by_id(comment_id)
        if comment.is_pinned:
            raise ValidationError("Comment is already pinned")

        # Unpin other pinned comments for this content
        pinned = self.repository.get_pinned_comments(comment.content_id)
        for pinned_comment in pinned:
            if pinned_comment.id != comment_id:
                self.repository.update(pinned_comment.id, {"is_pinned": False})

        return self.repository.pin_comment(comment_id)

    def _validate_create(self, obj_in: CommentCreate) -> None:
        """Validate comment creation"""
        if len(obj_in.content) < 3:
            raise ValidationError("Comment must be at least 3 characters")

        if len(obj_in.content) > 5000:
            raise ValidationError("Comment must be less than 5000 characters")