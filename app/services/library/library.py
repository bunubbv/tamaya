import aiofiles
import asyncio
from typing import Any
from fastapi import HTTPException, status
from core.database import NoResultFound
from core.logging import logs
from repos.library import LibraryRepo
from tools.path_handler import get_path


class LibraryService:
    semaphore = asyncio.Semaphore(5)

    def __init__(self, repo: LibraryRepo) -> None:
        self.repo = repo
        self.tags = {}


    async def get_tracks(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        tracks, total = await self.repo.get_tracks(start, end)
        return { "tracks": tracks, "total": total }


    async def get_track(self, track_id: str) -> dict[str, Any]:
        try:
            return await self.repo.get_track(track_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        

    async def get_albums(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        albums, total = await self.repo.get_albums(start, end)
        return { "albums": albums, "total": total }


    async def get_album(self, album_id: str) -> dict[str, list[dict[str, Any] | None] | Any]:
        try:
            return await self.repo.get_album(album_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    async def get_artists(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        artists, total = await self.repo.get_artists(start, end)
        return { "artists": artists, "total": total }


    async def get_artist(self, artist_id: str) -> dict[str, list[dict[str, Any]] | Any]:
        try:
            return await self.repo.get_artist(artist_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

    async def streaming(self, track_id: str, range: str) -> tuple[bytes, dict[str, Any]]:
        path = await self.repo.get_item_path(track_id)
        print(path)
        try:
            path = await self.repo.get_item_path(track_id)
            track_info = await self.repo.get_track(track_id)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        track_mime = track_info['content_type']
        track_size = track_info['filesize']
        track_chunk = int(track_size * 0.25)
        real_path = get_path(path)

        if range:
            track_range = range.replace("bytes=", "").split("-")
            track_start = int(track_range[0])
            track_end = int(track_range[1]) if track_range[1] else track_start + track_chunk
        else:
            track_start = 0
            track_end = track_start + track_chunk

        if track_start == 0:
            logs.debug("Playing \"%s\" (%s-%s)", track_info['title'], track_start, track_end)
            
        track_end = min(track_end, track_size - 1)

        async with aiofiles.open(real_path, mode="rb") as track_file:
            await track_file.seek(track_start)
            data = await track_file.read(track_end - track_start + 1)
            headers = {
                "Content-Range": f"bytes {track_start}-{track_end}/{track_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(track_end - track_start + 1),
                "Content-Type": track_mime
            }

            return data, headers
