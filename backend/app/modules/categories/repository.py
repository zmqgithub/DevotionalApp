from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.repositories.base import BaseRepository
from app.modules.categories.model import Category
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    """Repository for Category model"""

    def __init__(self, db: Session):
        super().__init__(db, Category)

    def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug"""
        return self.db.query(Category).filter(Category.slug == slug).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name"""
        return self.db.query(Category).filter(Category.name.ilike(name)).first()

    def get_root_categories(self) -> List[Category]:
        """Get all root categories (no parent)"""
        return self.db.query(Category).filter(
            Category.parent_id.is_(None),
            Category.is_active == True
        ).order_by(Category.order).all()

    def get_subcategories(self, parent_id: int) -> List[Category]:
        """Get all subcategories of a parent"""
        return self.db.query(Category).filter(
            Category.parent_id == parent_id,
            Category.is_active == True
        ).order_by(Category.order).all()

    def get_category_tree(self) -> List[Category]:
        """Get complete category tree"""
        return self.db.query(Category).filter(
            Category.parent_id.is_(None),
            Category.is_active == True
        ).order_by(Category.order).all()

    def get_active_categories(self) -> List[Category]:
        """Get all active categories"""
        return self.db.query(Category).filter(Category.is_active == True).all()

    def search_categories(self, search: str) -> List[Category]:
        """Search categories by name or slug"""
        return self.db.query(Category).filter(
            or_(
                Category.name.ilike(f"%{search}%"),
                Category.slug.ilike(f"%{search}%")
            ),
            Category.is_active == True
        ).all()