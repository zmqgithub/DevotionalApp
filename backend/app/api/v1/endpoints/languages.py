# app/api/v1/endpoints/languages.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.languages.service import LanguageService
from app.modules.languages.schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from app.api.v1.dependencies import get_current_superuser, require_admin
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[LanguageResponse])
async def get_languages(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        is_active: Optional[bool] = True,
        db: Session = Depends(get_db)
):
    """Get all languages"""
    service = LanguageService(db)

    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active

    languages = service.get_all(skip=skip, limit=limit, filters=filters)
    total = service.count(filters)

    return PaginatedResponse(
        items=languages,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/default", response_model=LanguageResponse)
async def get_default_language(
        db: Session = Depends(get_db)
):
    """Get default language"""
    service = LanguageService(db)
    language = service.get_default_language()
    if not language:
        raise HTTPException(status_code=404, detail="Default language not found")
    return language


@router.get("/{language_id}", response_model=LanguageResponse)
async def get_language(
        language_id: int,
        db: Session = Depends(get_db)
):
    """Get language by ID"""
    service = LanguageService(db)
    return service.get_by_id(language_id)


@router.get("/code/{code}", response_model=LanguageResponse)
async def get_language_by_code(
        code: str,
        db: Session = Depends(get_db)
):
    """Get language by code"""
    service = LanguageService(db)
    language = service.get_by_code(code)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language


@router.post("/", response_model=LanguageResponse)
async def create_language(
        language_data: LanguageCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Create a new language (admin only)"""
    service = LanguageService(db)
    return service.create(language_data)


@router.put("/{language_id}", response_model=LanguageResponse)
async def update_language(
        language_id: int,
        language_data: LanguageUpdate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    """Update a language (admin only)"""
    service = LanguageService(db)
    return service.update(language_id, language_data)


@router.post("/{language_id}/set-default")
async def set_default_language(
        language_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Set a language as default (super admin only)"""
    service = LanguageService(db)
    service.set_default_language(language_id)
    return MessageResponse(message="Default language set successfully")


@router.delete("/{language_id}")
async def delete_language(
        language_id: int,
        current_user: User = Depends(get_current_superuser),
        db: Session = Depends(get_db)
):
    """Delete a language (super admin only)"""
    service = LanguageService(db)
    service.delete(language_id)
    return MessageResponse(message="Language deleted successfully")