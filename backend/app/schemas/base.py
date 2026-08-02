from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from pydantic import Field

T = TypeVar('T')

class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra='ignore'
    )

class TimestampSchema(BaseSchema):
    """Schema with timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated response wrapper"""
    items: List[T]
    total: int
    page: int = Field(ge=1)
    size: int = Field(ge=1, le=100)
    pages: int

class MessageResponse(BaseSchema):
    """Simple message response"""
    message: str
    status: str = "success"

class ErrorResponse(BaseSchema):
    """Error response"""
    error: str
    detail: Optional[str] = None
    status_code: int