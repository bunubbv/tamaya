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
from models import Album, Artist, Track
from typing import Any

class LibraryRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def get_tracks(self, start: int, end: int) -> tuple[list[dict[str, Any]], int]:
        db_query = await self.conn.execute(
            select(
                Track.album,
                Track.album_id,
                Track.artist,
                Track.artist_id,
                Track.duration,
                Track.title,
                Track.track_id,
            )
            .order_by(Track.title.asc())
            .offset(start - 1)
            .limit(end - (start - 1))
        )
        track_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Track)
        )
        total = total_query.scalar_one()
        return track_list, total
    

    async def get_track(self, track_id: str) -> dict[str, Any]:
        track_item = {}
        db_query = await self.conn.execute(
            select(Track.__table__).where(Track.track_id == track_id)
        )
        track_item = db_query.mappings().first()

        if track_item:
            return dict(track_item)
        else:
            raise NoResultFound


    async def get_albums(self, start: int, end: int) -> tuple[list[dict[str, Any]], int]:
        album_query = await self.conn.execute(
            select(
                Album.album,
                Album.album_id,
                Artist.artist.label('albumartist'),
                Album.albumartist_id,
                Album.year,
            )
            .select_from(
                join(
                    Album, Artist,
                    Album.albumartist_id == Artist.artist_id
                )
            )
            .order_by(Album.album.asc())
            .offset(start - 1)
            .limit(end - (start - 1))
        )
        album_list = [dict(row) for row in album_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Album)
        )
        total = total_query.scalar_one()
        return album_list, total
    

    async def get_album(self, album_id: str) -> dict[str, list[dict[str, Any] | None] | Any]:
        album_item = {}
        album_query = await self.conn.execute(
            select(
                Album.__table__,
                Artist.artist.label('albumartist')
            )
            .select_from(
                join(
                    Album, Artist,
                    Album.albumartist_id == Artist.artist_id
                )
            )
            .where(Album.album_id == album_id)
        )
        
        album_item = album_query.mappings().first()
        if album_item:
            album_item = dict(album_item)
        else:
            raise NoResultFound

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
            .where(Track.album_id == album_id)
            .order_by(Track.track_number.asc())
        )
        album_item['tracks'] = [dict(row) for row in track_query.mappings().all()]
        return album_item


    async def get_artists(self, start: int, end: int) -> tuple[list[dict[str, Any]], int]:
        db_query = await self.conn.execute(
            select(Artist.__table__)
            .order_by(Artist.artist.asc())
            .offset(start - 1)
            .limit(end - (start - 1))
        )
        artist_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Artist)
        )
        total = total_query.scalar_one()
        return artist_list, total


    async def get_artist(self, artist_id: str) -> dict[str, list[dict[str, Any]] | Any]:
        artist_item = {}
        track_query = await self.conn.execute(
            select(Track.album_id)
            .where(or_(Track.artist_id == artist_id, Track.albumartist_id == artist_id))
        )
        tracks_data = track_query.mappings().all()

        if tracks_data:
            # 해당 아이템 있으면 album_id 사용하여 앨범 검색
            album_ids = [track['album_id'] for track in tracks_data]
            album_from_tracks_query = await self.conn.execute(
                select(
                    Album.album,
                    Album.album_id,
                    Album.albumartist_id,
                    Album.year,
                )
                .where(Album.album_id.in_(album_ids))
                .order_by(Album.year.asc())
            )
            
            albums_data = album_from_tracks_query.mappings().all()
            albums_data = [dict(album) for album in albums_data]

            if albums_data:
                album = albums_data[0]
                
                # 앨범 albumartist_id 이용하여 아티스트 조회
                artist_query = await self.conn.execute(
                    select(Artist.__table__)
                    .where(Artist.artist_id == album['albumartist_id'])
                )
                artist_data = artist_query.mappings().first()

                if artist_data:
                    artist_item = {
                        'artist': artist_data['artist'],
                        'artist_id': artist_id,
                        'album_total': artist_data['album_total'],
                        'track_total': artist_data['track_total'],
                        'duration_total': artist_data['duration_total'],
                        'filesize_total': artist_data['filesize_total'],
                        'albums': albums_data
                    }
        else:
            raise NoResultFound

        return artist_item
    

    async def get_scan_info(self) -> Any:
        result = await self.conn.execute(select(Track.filepath, Track.filesize))
        result = result.all()

        return result

    
    async def get_item_path(self, id: str) -> str:
        '''
        Get string path from album or track ID.
        '''

        result = await self.conn.execute(
            select(Track.filepath).where(or_(Track.track_id == id, Track.album_id == id))
        )

        row = result.scalars().first()
        return row if row else ''


    async def insert_track(self, track_data: dict[str, Any]) -> None:
        await self.conn.execute(
            insert(Track).values(**track_data)
        )


    async def insert_album(self, album_data: dict[str, Any]) -> None:
        await self.conn.execute(
            Insert(Album).values(**album_data).on_conflict_do_nothing()
        )


    async def insert_artist(self, artist_data: dict[str, Any]) -> None:
        await self.conn.execute(
            Insert(Artist)
            .values(**artist_data)
            .on_conflict_do_update(
                index_elements=['artist_id'],
                set_=artist_data
            )
        )


    async def delete_track(self, filepath: str) -> None:
        await self.conn.execute(
            delete(Track).where(Track.filepath == filepath)
        )


    async def delete_album(self, album_id: str) -> None:
        await self.conn.execute(
            delete(Album).where(Album.album_id == album_id)
        )


    async def delete_artist(self, artist_id: str) -> None:
        await self.conn.execute(
            delete(Artist).where(Artist.artist_id == artist_id)
        )
