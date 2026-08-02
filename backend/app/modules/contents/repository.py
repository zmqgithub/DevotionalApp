from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, Query
from sqlalchemy import or_, and_, func
from app.repositories.base import BaseRepository
from app.modules.contents.model import Content, ContentStatus, ContentType
from app.modules.contents.schemas import ContentCreate, ContentUpdate


class ContentRepository(BaseRepository[Content, ContentCreate, ContentUpdate]):
    """Repository for Content model"""

    def __init__(self, db: Session):
        super().__init__(db, Content)

    def get_by_slug(self, slug: str) -> Optional[Content]:
        """Get content by slug"""
        return self.db.query(Content).filter(Content.slug == slug).first()

    def get_by_category(self, category_id: int) -> List[Content]:
        """Get all content in a category"""
        return self.db.query(Content).filter(
            Content.category_id == category_id,
            Content.status == ContentStatus.PUBLISHED
        ).all()

    def get_by_type(self, content_type: ContentType) -> List[Content]:
        """Get content by type"""
        return self.db.query(Content).filter(
            Content.content_type == content_type,
            Content.status == ContentStatus.PUBLISHED
        ).all()

    def get_published_content(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Content]:
        """Get published content with filters"""
        query = self.db.query(Content).filter(Content.status == ContentStatus.PUBLISHED)

        if filters:
            for key, value in filters.items():
                if hasattr(Content, key) and value is not None:
                    query = query.filter(getattr(Content, key) == value)

        return query.offset(skip).limit(limit).all()

    def search_content(
            self,
            query_text: str,
            content_type: Optional[ContentType] = None,
            category_id: Optional[int] = None
    ) -> List[Content]:
        """Search content by title, description, or content"""
        query = self.db.query(Content).filter(
            or_(
                Content.title.ilike(f"%{query_text}%"),
                Content.description.ilike(f"%{query_text}%"),
                Content.content.ilike(f"%{query_text}%")
            ),
            Content.status == ContentStatus.PUBLISHED
        )

        if content_type:
            query = query.filter(Content.content_type == content_type)

        if category_id:
            query = query.filter(Content.category_id == category_id)

        return query.all()

    def increment_view_count(self, content_id: int) -> bool:
        """Increment view count for content"""
        content = self.get_by_id(content_id)
        if content:
            content.view_count += 1
            self.db.commit()
            return True
        return False

    def increment_like_count(self, content_id: int) -> bool:
        """Increment like count for content"""
        content = self.get_by_id(content_id)
        if content:
            content.like_count += 1
            self.db.commit()
            return True
        return False

    def get_featured_content(self, limit: int = 10) -> List[Content]:
        """Get featured content"""
        return self.db.query(Content).filter(
            Content.is_featured == True,
            Content.status == ContentStatus.PUBLISHED
        ).order_by(Content.created_at.desc()).limit(limit).all()

    def get_trending_content(self, limit: int = 10) -> List[Content]:
        """Get trending content (by views, likes, shares)"""
        return self.db.query(Content).filter(
            Content.status == ContentStatus.PUBLISHED
        ).order_by(
            (Content.view_count + Content.like_count + Content.share_count).desc()
        ).limit(limit).all()

    def get_content_with_relations(self, content_id: int) -> Optional[Content]:
        """Get content with all related data"""
        return self.db.query(Content).filter(Content.id == content_id).first()