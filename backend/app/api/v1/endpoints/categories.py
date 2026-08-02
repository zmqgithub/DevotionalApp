# app/api/v1/endpoints/categories.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.categories.service import CategoryService
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate, CategoryResponse, \
    CategoryWithChildrenResponse
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CategoryResponse])
async def get_categories(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        parent_id: Optional[int] = None,
        is_active: Optional[bool] = True,
        db: Session = Depends(get_db)
):
    """Get all categories"""
    service = CategoryService(db)

    if parent_id is not None:
        categories = service.get_subcategories(parent_id)
        total = len(categories)
    else:
        filters = {}
        if is_active is not None:
            filters['is_active'] = is_active
        if parent_id is not None:
            filters['parent_id'] = parent_id
        categories = service.get_all(skip=skip, limit=limit, filters=filters)
        total = service.count(filters)

    return PaginatedResponse(
        items=categories,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/tree", response_model=List[CategoryWithChildrenResponse])
async def get_category_tree(
        db: Session = Depends(get_db)
):
    """Get complete category tree"""
    service = CategoryService(db)
    return service.get_category_tree()


@router.get("/{category_id}", response_model=CategoryWithChildrenResponse)
async def get_category(
        category_id: int,
        db: Session = Depends(get_db)
):
    """Get category by ID with children"""
    service = CategoryService(db)
    return service.get_category_with_children(category_id)


@router.post("/", response_model=CategoryResponse)
async def create_category(
        category_data: CategoryCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new category (admin only)"""
    service = CategoryService(db)
    return service.create(category_data)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
        category_id: int,
        category_data: CategoryUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a category (admin only)"""
    service = CategoryService(db)
    return service.update(category_id, category_data)


@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a category (super admin only)"""
    service = CategoryService(db)
    service.delete(category_id)
    return MessageResponse(message="Category deleted successfully")