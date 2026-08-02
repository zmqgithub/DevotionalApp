from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.contents.repository import ContentRepository
from app.modules.contents.model import Content, ContentStatus, ContentType
from app.modules.contents.schemas import ContentCreate, ContentUpdate
from app.core.exceptions import ValidationError, DuplicateError


class ContentService(BaseService[Content, ContentCreate, ContentUpdate]):
    """Service for Content business logic"""

    def __init__(self, db: Session):
        self.repository = ContentRepository(db)
        super().__init__(self.repository)

    def get_by_slug(self, slug: str) -> Optional[Content]:
        """Get content by slug"""
        return self.repository.get_by_slug(slug)

    def get_by_category(self, category_id: int) -> List[Content]:
        """Get all content in a category"""
        return self.repository.get_by_category(category_id)

    def get_by_type(self, content_type: ContentType) -> List[Content]:
        """Get content by type"""
        return self.repository.get_by_type(content_type)

    def get_published_content(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Content]:
        """Get published content with filters"""
        return self.repository.get_published_content(skip=skip, limit=limit, filters=filters)

    def search_content(
            self,
            query: str,
            content_type: Optional[ContentType] = None,
            category_id: Optional[int] = None
    ) -> List[Content]:
        """Search content"""
        return self.repository.search_content(query, content_type, category_id)

    def publish_content(self, content_id: int) -> Content:
        """Publish content"""
        content = self.get_by_id(content_id)
        if content.status == ContentStatus.PUBLISHED:
            raise ValidationError("Content is already published")

        content.status = ContentStatus.PUBLISHED
        content.published_at = datetime.utcnow()
        return self.repository.update(content_id, content)

    def unpublish_content(self, content_id: int) -> Content:
        """Unpublish content"""
        content = self.get_by_id(content_id)
        if content.status != ContentStatus.PUBLISHED:
            raise ValidationError("Content is not published")

        content.status = ContentStatus.DRAFT
        content.published_at = None
        return self.repository.update(content_id, content)

    def archive_content(self, content_id: int) -> Content:
        """Archive content"""
        content = self.get_by_id(content_id)
        if content.status == ContentStatus.ARCHIVED:
            raise ValidationError("Content is already archived")

        content.status = ContentStatus.ARCHIVED
        return self.repository.update(content_id, content)

    def increment_view_count(self, content_id: int) -> bool:
        """Increment view count"""
        return self.repository.increment_view_count(content_id)

    def increment_like_count(self, content_id: int) -> bool:
        """Increment like count"""
        return self.repository.increment_like_count(content_id)

    def get_featured_content(self, limit: int = 10) -> List[Content]:
        """Get featured content"""
        return self.repository.get_featured_content(limit)

    def get_trending_content(self, limit: int = 10) -> List[Content]:
        """Get trending content"""
        return self.repository.get_trending_content(limit)

    def get_content_with_relations(self, content_id: int) -> Content:
        """Get content with all related data"""
        content = self.repository.get_content_with_relations(content_id)
        if not content:
            raise NotFoundError(f"Content with ID {content_id} not found")
        return content

    def _validate_create(self, obj_in: ContentCreate) -> None:
        """Validate content creation"""
        if not obj_in.title:
            raise ValidationError("Title is required")

        if not obj_in.slug:
            raise ValidationError("Slug is required")

        if len(obj_in.slug) < 3:
            raise ValidationError("Slug must be at least 3 characters")

    def _check_duplicate_on_create(self, obj_in: ContentCreate) -> None:
        """Check for duplicate content"""
        if self.repository.get_by_slug(obj_in.slug):
            raise DuplicateError(f"Content with slug {obj_in.slug} already exists")

    def _check_duplicate_on_update(self, obj_in: ContentUpdate, id: int) -> None:
        """Check for duplicate content on update"""
        if hasattr(obj_in, 'slug') and obj_in.slug:
            existing = self.repository.get_by_slug(obj_in.slug)
            if existing and existing.id != id:
                raise DuplicateError(f"Content with slug {obj_in.slug} already exists")