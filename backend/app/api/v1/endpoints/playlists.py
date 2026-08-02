from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.playlists.service import PlaylistService
from app.modules.playlists.schemas import (
    PlaylistCreate, PlaylistUpdate, PlaylistResponse, PlaylistDetailResponse
)
from app.api.v1.dependencies import get_current_user
from app.modules.users.model import User
from app.schemas.base import PaginatedResponse, MessageResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[PlaylistResponse])
async def get_playlists(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        is_public: bool = Query(True),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get playlists"""
    service = PlaylistService(db)

    if is_public:
        playlists = service.get_public_playlists(skip, limit)
        total = service.count({'is_public': True})
    else:
        playlists = service.get_by_user(current_user.id)
        total = len(playlists)

    return PaginatedResponse(
        items=playlists,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/me", response_model=List[PlaylistResponse])
async def get_my_playlists(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get current user's playlists"""
    service = PlaylistService(db)
    return service.get_by_user(current_user.id)


@router.get("/{playlist_id}", response_model=PlaylistDetailResponse)
async def get_playlist(
        playlist_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get playlist by ID with items"""
    service = PlaylistService(db)
    playlist = service.get_playlist_with_items(playlist_id)

    # Check if playlist is private and user is not owner
    if not playlist.is_public and playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This playlist is private"
        )

    return playlist


@router.post("/", response_model=PlaylistResponse)
async def create_playlist(
        playlist_data: PlaylistCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create a new playlist"""
    service = PlaylistService(db)
    playlist_data.user_id = current_user.id
    return service.create(playlist_data)


@router.put("/{playlist_id}", response_model=PlaylistResponse)
async def update_playlist(
        playlist_id: int,
        playlist_data: PlaylistUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update a playlist"""
    service = PlaylistService(db)
    playlist = service.get_by_id(playlist_id)

    if playlist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this playlist"
        )

    return service.update(playlist_id, playlist_data)


@router.delete("/{playlist_id}")
async def delete_playlist(
        playlist_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Delete a playlist"""
    service = PlaylistService(db)
    playlist = service.get_by_id(playlist_id)

    if playlist.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this playlist"
        )

    service.delete(playlist_id)
    return MessageResponse(message="Playlist deleted successfully")


@router.post("/{playlist_id}/items/{content_id}")
async def add_item_to_playlist(
        playlist_id: int,
        content_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Add content to playlist"""
    service = PlaylistService(db)
    playlist = service.get_by_id(playlist_id)

    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this playlist"
        )

    service.add_item_to_playlist(playlist_id, content_id)
    return MessageResponse(message="Item added to playlist successfully")


@router.delete("/{playlist_id}/items/{item_id}")
async def remove_item_from_playlist(
        playlist_id: int,
        item_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Remove item from playlist"""
    service = PlaylistService(db)
    playlist = service.get_by_id(playlist_id)

    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this playlist"
        )

    service.remove_item_from_playlist(playlist_id, item_id)
    return MessageResponse(message="Item removed from playlist successfully")


@router.put("/{playlist_id}/reorder")
async def reorder_playlist_items(
        playlist_id: int,
        item_ids: List[int],
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Reorder playlist items"""
    service = PlaylistService(db)
    playlist = service.get_by_id(playlist_id)

    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this playlist"
        )

    service.reorder_items(playlist_id, item_ids)
    return MessageResponse(message="Playlist reordered successfully")