from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.modules.playlists.playlist_items.model import PlaylistItem
from app.modules.playlists.playlist_items.schemas import PlaylistItemCreate, PlaylistItemUpdate


class PlaylistItemRepository(BaseRepository[PlaylistItem, PlaylistItemCreate, PlaylistItemUpdate]):
    """Repository for PlaylistItem model"""

    def __init__(self, db: Session):
        super().__init__(db, PlaylistItem)

    def get_by_playlist(self, playlist_id: int) -> List[PlaylistItem]:
        """Get all items in a playlist"""
        return self.db.query(PlaylistItem).filter(
            PlaylistItem.playlist_id == playlist_id
        ).order_by(PlaylistItem.order).all()

    def get_by_content(self, content_id: int) -> List[PlaylistItem]:
        """Get all playlists containing a content item"""
        return self.db.query(PlaylistItem).filter(
            PlaylistItem.content_id == content_id
        ).all()

    def get_item_order(self, playlist_id: int) -> int:
        """Get the next order number for a playlist"""
        max_order = self.db.query(PlaylistItem.order).filter(
            PlaylistItem.playlist_id == playlist_id
        ).order_by(PlaylistItem.order.desc()).first()

        return (max_order[0] + 1) if max_order else 0

    def reorder_items(self, playlist_id: int, item_ids: List[int]) -> bool:
        """Reorder items in a playlist"""
        for index, item_id in enumerate(item_ids):
            self.db.query(PlaylistItem).filter(
                PlaylistItem.id == item_id,
                PlaylistItem.playlist_id == playlist_id
            ).update({"order": index})

        self.db.commit()
        return True

    def remove_content_from_playlists(self, content_id: int) -> bool:
        """Remove a content item from all playlists"""
        self.db.query(PlaylistItem).filter(
            PlaylistItem.content_id == content_id
        ).delete()
        self.db.commit()
        return True