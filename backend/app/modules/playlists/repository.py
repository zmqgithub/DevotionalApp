from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.playlists.model import Playlist
from app.modules.playlists.schemas import PlaylistCreate, PlaylistUpdate


class PlaylistRepository(BaseRepository[Playlist, PlaylistCreate, PlaylistUpdate]):
    """Repository for Playlist model"""

    def __init__(self, db: Session):
        super().__init__(db, Playlist)

    def get_by_user(self, user_id: int) -> List[Playlist]:
        """Get all playlists for a user"""
        return self.db.query(Playlist).filter(
            Playlist.user_id == user_id,
            Playlist.is_active == True
        ).all()

    def get_public_playlists(self, skip: int = 0, limit: int = 100) -> List[Playlist]:
        """Get all public playlists"""
        return self.db.query(Playlist).filter(
            Playlist.is_public == True,
            Playlist.is_active == True
        ).offset(skip).limit(limit).all()

    def get_playlist_with_items(self, playlist_id: int) -> Optional[Playlist]:
        """Get playlist with its items"""
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()

    def search_playlists(self, search: str) -> List[Playlist]:
        """Search playlists by name"""
        return self.db.query(Playlist).filter(
            Playlist.name.ilike(f"%{search}%"),
            Playlist.is_public == True,
            Playlist.is_active == True
        ).all()