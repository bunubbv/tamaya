import uuid
from datetime import datetime
from typing import Any
from fastapi import HTTPException, status
from core.database import NoResultFound
from core.logging import logs
from models.playlist import PlaylistModel, PlaylistCreateModel
from repos.playlist import PlaylistRepo


class PlaylistService:
    def __init__(self, repo: PlaylistRepo) -> None:
        self.repo = repo

    
    async def get_playlists(self, user_id: str, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        playlists, total = await self.repo.get_playlists(user_id, start, end)
        return {
            "playlists": playlists,
            "total": total
        }

    
    async def get_playlist(self, playlist_id: str, start: int, end: int) -> dict[str, list[dict[str, Any] | None] | Any]:
        try:
            return await self.repo.get_playlist(playlist_id, start, end)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    async def create_playlist(self, data: PlaylistCreateModel, user_id) -> None:
        playlist_item = {
            "playlist_id": str(uuid.uuid4()),
            "playlist_name": data.playlist_name,
            "playlist_user": user_id,
            "shared": data.shared,
        }

        await self.repo.create_playlist(playlist_item)


    async def delete_playlist(self, playlist_id: str) -> None:
        await self.repo.delete_playlist(playlist_id)
