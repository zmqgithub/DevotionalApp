from fastapi import APIRouter
from app.api.v1.endpoints import (
    users,
    roles,
    permissions,
    countries,
    states,
    cities,
    languages,
    categories,
    contents,
    playlists,
    comments,
    favorites,
    ratings,
    mosques,
    events,
    notifications,
    uploads,
    announcements,
    audit,
    schedules,
    recitations,
    auth,
    health
)

api_router = APIRouter()

# Health check
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# User Management
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])

# Location
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(states.router, prefix="/states", tags=["states"])
api_router.include_router(cities.router, prefix="/cities", tags=["cities"])
api_router.include_router(languages.router, prefix="/languages", tags=["languages"])

# Content
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(recitations.router, prefix="/recitations", tags=["recitations"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])

# User Interactions
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])

# Mosque & Events
api_router.include_router(mosques.router, prefix="/mosques", tags=["mosques"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])

# System
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["announcements"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])