# app/db/base.py
from app.db.base_class import Base

# Import all models so Alembic can detect them
# These imports should be here but AFTER Base is defined
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.modules.permissions.model import Permission
from app.modules.roles.user_role.model import UserRole
from app.modules.roles.role_permission.model import RolePermission

# Location modules
from app.modules.countries.model import Country
from app.modules.states.model import State
from app.modules.cities.model import City
from app.modules.languages.model import Language
from app.modules.currencies.model import Currency
from app.modules.countries_languages.model import CountryLanguage

# Content modules
from app.modules.categories.model import Category
from app.modules.contents.model import Content
from app.modules.recitations.model import Recitation

# User interaction modules
from app.modules.playlists.model import Playlist
from app.modules.playlists.playlist_items.model import PlaylistItem
from app.modules.favorites.model import Favorite
from app.modules.ratings.model import Rating
from app.modules.comments.model import Comment
from app.modules.dedications.model import Dedication
from app.modules.recent_history.model import RecentHistory

# Mosque and related modules
from app.modules.mosques.model import Mosque
from app.modules.events.model import Event
from app.modules.schedules.model import Schedule

# System modules
from app.modules.notifications.model import Notification
from app.modules.uploads.model import Upload
from app.modules.settings.model import Setting
from app.modules.announcements.model import Announcement
from app.modules.audit.model import AuditLog

__all__ = ["Base"]