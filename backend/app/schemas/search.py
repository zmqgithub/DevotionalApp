from pydantic import Field
from typing import Optional, List
from app.schemas.base import BaseSchema

class SearchRequest(BaseSchema):
    query: str = Field(..., min_length=1)
    content_type: Optional[str] = None
    category_id: Optional[int] = None
    language_id: Optional[int] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    is_premium: Optional[bool] = None
    tags: Optional[List[str]] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="relevance", pattern="^(relevance|date|rating|views)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")