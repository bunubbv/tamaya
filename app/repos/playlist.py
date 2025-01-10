from typing import Any
from models import Playlist, PlaylistData, Track
from models.playlist import (
    PlaylistModel,
    PlaylistDataModel
)
from core.database import (
    AsyncConnection,
    select,
    insert,
    Insert,
    delete,
    NoResultFound,
    or_,
    join,
    func,
)

class PlaylistRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

    
    async def get_playlists(self, user_id: str, start: int, end: int) -> tuple[list[dict[str, Any]], int]:
        db_query = await self.conn.execute(
            select(Playlist.__table__)
            .order_by(Playlist.playlist_name.asc())
            .offset(start - 1)
            .limit(end - (start - 1))
            .where(Playlist.playlist_user == user_id)
        )
        playlist_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count())
            .select_from(Playlist)
            .where(Playlist.playlist_user == user_id)
        )
        total = total_query.scalar_one()
        return playlist_list, total


    async def get_playlist(self, playlist_id: str, start: int, end: int) -> dict[str, list[dict[str, Any] | None] | Any]:
        playlist_item = {}
        playlist_query = await self.conn.execute(
            select(Playlist.__table__)
            .where(Playlist.playlist_id == playlist_id)
        )
        playlist_item = playlist_query.mappings().first()

        if not playlist_item:
            raise NoResultFound

        playlist_item = dict(playlist_item)
        track_query = await self.conn.execute(
            select(
                Track.artist,
                Track.artist_id,
                Track.comment,
                Track.duration,
                Track.title,
                Track.track_id,
                Track.track_number,
            )
            .join(PlaylistData, PlaylistData.track_id == Track.track_id)
            .where(PlaylistData.playlist_id == playlist_id)
            .order_by(Track.track_number.asc())
            .offset(start)
            .limit(end - start)
        )

        playlist_item['tracks'] = [dict(row) for row in track_query.mappings().all()]

        return playlist_item


    async def create_playlist(self, playlist_data: dict[str, Any]) -> None:
        await self.conn.execute(
            insert(Playlist).values(**playlist_data)
        )


    async def delete_playlist(self, playlist_id: str) -> None:
        await self.conn.execute(
            delete(Playlist).where(Playlist.playlist_id == playlist_id)
        )
