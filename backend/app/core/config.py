from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "DevotionalApp API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_EXPIRE_HOURS: int = 24
    EMAIL_VERIFICATION_EXPIRE_DAYS: int = 7

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "devotional_user"
    POSTGRES_PASSWORD: str = "devotional_password"
    POSTGRES_DB: str = "devotional_db"
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str, info) -> str:
        if v and isinstance(v, str):
            return v

        data = info.data if hasattr(info, 'data') else {}
        postgres_user = data.get('POSTGRES_USER', 'devotional_user')
        postgres_password = data.get('POSTGRES_PASSWORD', 'devotional_password')
        postgres_server = data.get('POSTGRES_SERVER', 'localhost')
        postgres_db = data.get('POSTGRES_DB', 'devotional_db')

        return f"postgresql://{postgres_user}:{postgres_password}@{postgres_server}/{postgres_db}"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080"
    ]

    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None

    # Redis (for caching)
    REDIS_URL: Optional[str] = None

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()