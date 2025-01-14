import asyncio
from models import Album, Artist, Track
from core.database import db_conn, select, func, exists
from core.logging import logs
from repos.library import LibraryRepo


class LibraryScan:
    @staticmethod
    async def perform_all() -> None:
        await asyncio.gather(
            LibraryScan.perform_albums(),
            LibraryScan.perform_artists(),
            return_exceptions=True,
        )


    @staticmethod
    async def perform_albums() -> None:
        async with db_conn() as conn:
            db_query = (
                select(
                    Track.album,
                    Track.album_id,
                    Track.albumartist,
                    Track.albumartist_id,
                    Track.disc_total,
                    Track.track_total,
                    Track.year,
                    func.sum(Track.duration).label('duration_total'),
                    func.sum(Track.filesize).label('filesize_total'),
                )
                .where(
                    Track.album_id != '',
                )
                .group_by(
                    Track.album,
                    Track.album_id,
                    Track.albumartist,
                    Track.track_total,
                )
            )

            db_result = await conn.execute(db_query)
            albums_data = db_result.all()

            for alb in albums_data:
                album_data = {
                    'album': alb.album,
                    'album_id': alb.album_id,
                    'albumartist_id': alb.albumartist_id,
                    'disc_total': alb.disc_total,
                    'duration_total': alb.duration_total,
                    'filesize_total': alb.filesize_total,
                    'year': alb.year,
                }

                await LibraryRepo(conn).insert_album(album_data)

            unknown_query = (
                select(
                    Track.album,
                    Track.album_id,
                    Track.artist,
                    Track.disc_total,
                    Track.track_total,
                    Track.year,
                    func.sum(Track.duration).label('duration_total'),
                    func.sum(Track.filesize).label('filesize_total'),
                )
                .where(Track.album == '')
                .group_by(
                    Track.artist,
                    Track.directory,
                )
            )

            unknown_result = await conn.execute(unknown_query)
            unknown_albums_data = unknown_result.all()

            for alb in unknown_albums_data:
                album_data = {
                    'album': alb.album,
                    'album_id': alb.album_id,
                    'albumartist_id': '',
                    'disc_total': alb.disc_total,
                    'duration_total': alb.duration_total,
                    'filesize_total': alb.filesize_total,
                    'year': alb.year,
                }

                await LibraryRepo(conn).insert_album(album_data)

        async with db_conn() as conn:
            albums_query = select(Album.album_id)
            result = await conn.execute(albums_query)
            album_hash = {row.album_id for row in result}

            tracks_query = select(Track.album_id).distinct()
            result = await conn.execute(tracks_query)
            track_hash = {row.album_id for row in result}

            orphan_albums = album_hash - track_hash

            for album_id in orphan_albums:
                logs.debug("Removing Album... (%s)", album_id)
                await LibraryRepo(conn).delete_album(album_id)


    @staticmethod
    async def perform_artists() -> None:
        async with db_conn() as conn:
            db_query = (
                select(
                    Track.albumartist_id,
                    Track.albumartist,
                    func.count(Track.track_id).label('track_total'),
                    func.count(func.distinct(Track.album_id)).label('album_total'),
                    func.sum(Track.duration).label('duration_total'),
                    func.sum(Track.filesize).label('filesize_total'),
                )
                .where(Track.albumartist != '')
                .group_by(Track.albumartist_id, Track.albumartist)
            )

            db_result = await conn.execute(db_query)
            artists_data = db_result.all()

            for art in artists_data:
                artist_data = {
                    'artist': art.albumartist,
                    'artist_id': art.albumartist_id,
                    'album_total': art.album_total,
                    'track_total': art.track_total,
                    'duration_total': art.duration_total,
                    'filesize_total': art.filesize_total,
                }

                await LibraryRepo(conn).insert_artist(artist_data)

        async with db_conn() as conn:
            orphan_albumartists_query = (
                select(Artist.artist_id)
                .where(
                    ~exists(
                        select(1)
                        .where(Track.albumartist_id == Artist.artist_id)
                    )
                )
            )

            result = await conn.execute(orphan_albumartists_query)
            orphan_albumartists = {row[0] for row in result}

            for artist_id in orphan_albumartists:
                logs.debug("Removing Artist... (%s)", artist_id)
                await LibraryRepo(conn).delete_artist(artist_id)
