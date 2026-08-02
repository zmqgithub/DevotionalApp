from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.comments.service import CommentService
from app.modules.comments.schemas import CommentCreate, CommentUpdate, CommentResponse
from app.api.v1.dependencies import get_current_user, get_current_superuser
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/content/{content_id}", response_model=List[CommentResponse])
async def get_content_comments(
        content_id: int,
        db: Session = Depends(get_db)
):
    """Get all comments for a content"""
    service = CommentService(db)
    return service.get_by_content(content_id)


@router.post("/", response_model=CommentResponse)
async def create_comment(
        comment_data: CommentCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create a new comment"""
    service = CommentService(db)
    return service.create_comment(
        user_id=current_user.id,
        content_id=comment_data.content_id,
        text=comment_data.content
    )


@router.post("/{comment_id}/reply", response_model=CommentResponse)
async def reply_to_comment(
        comment_id: int,
        content: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Reply to a comment"""
    service = CommentService(db)
    return service.reply_to_comment(
        user_id=current_user.id,
        parent_id=comment_id,
        text=content
    )


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
        comment_id: int,
        comment_data: CommentUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update a comment"""
    service = CommentService(db)
    comment = service.get_by_id(comment_id)

    if comment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this comment"
        )

    return service.update(comment_id, comment_data)


@router.delete("/{comment_id}")
async def delete_comment(
        comment_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete a comment"""
    service = CommentService(db)
    comment = service.get_by_id(comment_id)

    if comment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this comment"
        )

    service.delete(comment_id)
    return MessageResponse(message="Comment deleted successfully")


@router.post("/{comment_id}/approve", response_model=CommentResponse)
async def approve_comment(
        comment_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Approve a comment (admin only)"""
    service = CommentService(db)
    return service.approve_comment(comment_id)


@router.post("/{comment_id}/pin", response_model=CommentResponse)
async def pin_comment(
        comment_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Pin a comment (admin only)"""
    service = CommentService(db)
    return service.pin_comment(comment_id)