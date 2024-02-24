from infra.setup_logger import *
from databases import Database
import sqlalchemy

DATABASE_URL = "sqlite:///" + get_strpath('config', 'tamaya.db', rel=False)
metadata = sqlalchemy.MetaData()

tracks = sqlalchemy.Table(
    "tracks",
    metadata,
    sqlalchemy.Column("album", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("albumsort", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("albumartist", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("albumartistsort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artistid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("artistsort", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("barcode", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("bitrate", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("bpm", sqlalchemy.Integer, nullable=False),
    # sqlalchemy.Column("catalognumber", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("channels", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("comment", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("compilation", sqlalchemy.Boolean(False), nullable=False),
    sqlalchemy.Column("composer", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("composersort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("conductor", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("contentgroup", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("copyright", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("createdate", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("date", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("dir", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("discnumber", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("disctotal", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("duration", sqlalchemy.REAL, nullable=False),
    sqlalchemy.Column("genre", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("grouping", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("id", sqlalchemy.String(''), nullable=False, primary_key=True),
    # sqlalchemy.Column("involved_people", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("imageid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("isrc", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("label", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("language", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("lyricist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("lyrics", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("mime", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("mix_artist", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_albumartistid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_albumid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_albumtype", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_artistid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_discid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_originalalbumid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_originalartistid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_releasegroupid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_releasetrackid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_trackid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("orignalalbum", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("orignalartist", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("orignallyricist", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("orignalyear", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("path", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("publisher", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("releasetype", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("releasetime", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("samplerate", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("script", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("setsubtitle", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    # sqlalchemy.Column("subtitle", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("titlesort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("tracknumber", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("tracktotal", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("year", sqlalchemy.Integer, nullable=False),
)
albums = sqlalchemy.Table(
    "albums",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artistid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumartist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumartistid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("tracknumber", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("createdate", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("duration", sqlalchemy.REAL, nullable=False),
    sqlalchemy.Column("dateafter", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("datebefore", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("dir", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("yearafter", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("yearbefore", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("imagepath", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("imageid", sqlalchemy.Integer, nullable=False),
)

if not get_path('config', 'tamaya.db', rel=False).exists():
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    db = Database(DATABASE_URL)
    logs.info("Creating new database...")
else:
    db = Database(DATABASE_URL)

async def connect_database():
    await db.connect()
    logs.info("Connected to database successfully.")

async def disconnect_database():
    await db.disconnect()