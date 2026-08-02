from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.comments.model import Comment
from app.modules.comments.schemas import CommentCreate, CommentUpdate


class CommentRepository(BaseRepository[Comment, CommentCreate, CommentUpdate]):
    """Repository for Comment model"""

    def __init__(self, db: Session):
        super().__init__(db, Comment)

    def get_by_content(self, content_id: int) -> List[Comment]:
        """Get all comments for a content item"""
        return self.db.query(Comment).filter(
            Comment.content_id == content_id,
            Comment.parent_id.is_(None),
            Comment.is_approved == True
        ).order_by(Comment.created_at.desc()).all()

    def get_by_user(self, user_id: int) -> List[Comment]:
        """Get all comments by a user"""
        return self.db.query(Comment).filter(
            Comment.user_id == user_id
        ).order_by(Comment.created_at.desc()).all()

    def get_replies(self, comment_id: int) -> List[Comment]:
        """Get all replies to a comment"""
        return self.db.query(Comment).filter(
            Comment.parent_id == comment_id,
            Comment.is_approved == True
        ).order_by(Comment.created_at.asc()).all()

    def approve_comment(self, comment_id: int) -> Optional[Comment]:
        """Approve a comment"""
        comment = self.get_by_id(comment_id)
        if comment:
            comment.is_approved = True
            self.db.commit()
            self.db.refresh(comment)
        return comment

    def pin_comment(self, comment_id: int) -> Optional[Comment]:
        """Pin a comment"""
        comment = self.get_by_id(comment_id)
        if comment:
            comment.is_pinned = True
            self.db.commit()
            self.db.refresh(comment)
        return comment

    def get_pinned_comments(self, content_id: int) -> List[Comment]:
        """Get pinned comments for content"""
        return self.db.query(Comment).filter(
            Comment.content_id == content_id,
            Comment.is_pinned == True,
            Comment.is_approved == True
        ).all()