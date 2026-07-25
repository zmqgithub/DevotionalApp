from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    profile_image_url: str | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    profile_image_url: str | None = None


class ChangePasswordRequest(BaseModel):

    current_password: str

    new_password: str


class UserStatusUpdate(BaseModel):

    is_active: bool


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    profile_image_url: str | None = None
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserListResponse(BaseModel):

    items: list[UserResponse]

    total: int

    page: int

    page_size: int

    total_pages: int