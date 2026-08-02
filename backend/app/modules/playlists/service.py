from typing import Optional, List
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.modules.playlists.repository import PlaylistRepository
from app.modules.playlists.model import Playlist
from app.modules.playlists.schemas import PlaylistCreate, PlaylistUpdate
from app.core.exceptions import ValidationError, NotFoundError


class PlaylistService(BaseService[Playlist, PlaylistCreate, PlaylistUpdate]):
    """Service for Playlist business logic"""

    def __init__(self, db: Session):
        self.repository = PlaylistRepository(db)
        super().__init__(self.repository)

    def get_by_user(self, user_id: int) -> List[Playlist]:
        """Get all playlists for a user"""
        return self.repository.get_by_user(user_id)

    def get_public_playlists(self, skip: int = 0, limit: int = 100) -> List[Playlist]:
        """Get all public playlists"""
        return self.repository.get_public_playlists(skip=skip, limit=limit)

    def get_playlist_with_items(self, playlist_id: int) -> Playlist:
        """Get playlist with its items"""
        playlist = self.repository.get_playlist_with_items(playlist_id)
        if not playlist:
            raise NotFoundError(f"Playlist with ID {playlist_id} not found")
        return playlist

    def add_item_to_playlist(self, playlist_id: int, content_id: int) -> bool:
        """Add an item to a playlist"""
        from app.modules.playlists.playlist_items.repository import PlaylistItemRepository
        from app.modules.playlists.playlist_items.schemas import PlaylistItemCreate

        playlist = self.get_by_id(playlist_id)
        if not playlist.is_active:
            raise ValidationError("Playlist is not active")

        # Get the next order number
        item_repo = PlaylistItemRepository(self.repository.db)
        order = item_repo.get_item_order(playlist_id)

        item_data = PlaylistItemCreate(
            playlist_id=playlist_id,
            content_id=content_id,
            order=order
        )

        item_repo.create(item_data)
        return True

    def remove_item_from_playlist(self, playlist_id: int, item_id: int) -> bool:
        """Remove an item from a playlist"""
        from app.modules.playlists.playlist_items.repository import PlaylistItemRepository

        item_repo = PlaylistItemRepository(self.repository.db)
        item = item_repo.get_by_id(item_id)
        if not item or item.playlist_id != playlist_id:
            raise NotFoundError(f"Item with ID {item_id} not found in playlist")

        return item_repo.delete(item_id)

    def reorder_items(self, playlist_id: int, item_ids: List[int]) -> bool:
        """Reorder items in a playlist"""
        playlist = self.get_by_id(playlist_id)

        # Verify all items belong to this playlist
        from app.modules.playlists.playlist_items.repository import PlaylistItemRepository
        item_repo = PlaylistItemRepository(self.repository.db)

        for item_id in item_ids:
            item = item_repo.get_by_id(item_id)
            if not item or item.playlist_id != playlist_id:
                raise ValidationError(f"Item with ID {item_id} does not belong to this playlist")

        return item_repo.reorder_items(playlist_id, item_ids)

    def _validate_delete(self, id: int) -> None:
        """Validate playlist deletion"""
        playlist = self.get_by_id(id)
        if not playlist.is_active:
            raise ValidationError("Playlist is already deleted")