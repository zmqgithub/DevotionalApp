from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.model import Category
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate
from app.core.exceptions import DuplicateError, ValidationError, NotFoundError


class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
    """Service for Category business logic"""

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)
        super().__init__(self.repository)

    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug"""
        return self.repository.get_by_slug(slug)

    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name"""
        return self.repository.get_by_name(name)

    def get_root_categories(self) -> List[Category]:
        """Get all root categories (no parent)"""
        return self.repository.get_root_categories()

    def get_subcategories(self, parent_id: int) -> List[Category]:
        """Get all subcategories of a parent"""
        parent = self.get_by_id(parent_id)
        return self.repository.get_subcategories(parent_id)

    def get_category_tree(self) -> List[Category]:
        """Get complete category tree"""
        return self.repository.get_category_tree()

    def get_active_categories(self) -> List[Category]:
        """Get all active categories"""
        return self.repository.get_active_categories()

    def search_categories(self, search: str) -> List[Category]:
        """Search categories by name or slug"""
        return self.repository.search_categories(search)

    def get_category_with_children(self, category_id: int) -> Category:
        """Get category with its children"""
        category = self.get_by_id(category_id)
        # Children will be loaded via relationship
        return category

    def _validate_create(self, obj_in: CategoryCreate) -> None:
        """Validate category creation"""
        if obj_in.parent_id:
            parent = self.get_by_id(obj_in.parent_id)
            if not parent:
                raise ValidationError(f"Parent category with ID {obj_in.parent_id} not found")

    def _check_duplicate_on_create(self, obj_in: CategoryCreate) -> None:
        """Check for duplicate category"""
        if self.repository.get_by_slug(obj_in.slug):
            raise DuplicateError(f"Category with slug {obj_in.slug} already exists")

        if self.repository.get_by_name(obj_in.name):
            raise DuplicateError(f"Category with name {obj_in.name} already exists")

    def _check_duplicate_on_update(self, obj_in: CategoryUpdate, id: int) -> None:
        """Check for duplicate category on update"""
        if hasattr(obj_in, 'slug') and obj_in.slug:
            existing = self.repository.get_by_slug(obj_in.slug)
            if existing and existing.id != id:
                raise DuplicateError(f"Category with slug {obj_in.slug} already exists")

        if hasattr(obj_in, 'name') and obj_in.name:
            existing = self.repository.get_by_name(obj_in.name)
            if existing and existing.id != id:
                raise DuplicateError(f"Category with name {obj_in.name} already exists")