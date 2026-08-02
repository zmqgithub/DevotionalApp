from typing import Generator
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

# Import all services
from app.modules.users.service import UserService
from app.modules.roles.service import RoleService
from app.modules.permissions.service import PermissionService
from app.modules.countries.service import CountryService
from app.modules.states.service import StateService
from app.modules.cities.service import CityService
from app.modules.languages.service import LanguageService
from app.modules.categories.service import CategoryService
from app.modules.contents.service import ContentService
from app.modules.playlists.service import PlaylistService
from app.modules.comments.service import CommentService
from app.modules.favorites.service import FavoriteService
from app.modules.ratings.service import RatingService
from app.modules.mosques.service import MosqueService
from app.modules.events.service import EventService
from app.modules.notifications.service import NotificationService
from app.modules.uploads.service import UploadService
from app.modules.announcements.service import AnnouncementService
from app.modules.audit.service import AuditService
from app.modules.schedules.service import ScheduleService
from app.modules.recitations.service import RecitationService

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User services
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)

def get_permission_service(db: Session = Depends(get_db)) -> PermissionService:
    return PermissionService(db)

# Location services
def get_country_service(db: Session = Depends(get_db)) -> CountryService:
    return CountryService(db)

def get_state_service(db: Session = Depends(get_db)) -> StateService:
    return StateService(db)

def get_city_service(db: Session = Depends(get_db)) -> CityService:
    return CityService(db)

def get_language_service(db: Session = Depends(get_db)) -> LanguageService:
    return LanguageService(db)

# Content services
def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)

def get_content_service(db: Session = Depends(get_db)) -> ContentService:
    return ContentService(db)

def get_playlist_service(db: Session = Depends(get_db)) -> PlaylistService:
    return PlaylistService(db)

def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db)

def get_favorite_service(db: Session = Depends(get_db)) -> FavoriteService:
    return FavoriteService(db)

def get_rating_service(db: Session = Depends(get_db)) -> RatingService:
    return RatingService(db)

def get_recitation_service(db: Session = Depends(get_db)) -> RecitationService:
    return RecitationService(db)

# Mosque and Event services
def get_mosque_service(db: Session = Depends(get_db)) -> MosqueService:
    return MosqueService(db)

def get_event_service(db: Session = Depends(get_db)) -> EventService:
    return EventService(db)

def get_schedule_service(db: Session = Depends(get_db)) -> ScheduleService:
    return ScheduleService(db)

# System services
def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)

def get_upload_service(db: Session = Depends(get_db)) -> UploadService:
    return UploadService(db)

def get_announcement_service(db: Session = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(db)

def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(db)