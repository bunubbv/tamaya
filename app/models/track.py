from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, Text, func
)
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from core.database import Base
from typing import Optional


class Track(Base):
    __tablename__ = 'tracks'

    album: str = Column(String, ForeignKey('albums.album'), nullable=False)
    album_id: str = Column(String(32), nullable=False)
    albumartist: str = Column(String, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), nullable=False)
    barcode: str = Column(String, nullable=False)
    bitdepth: int = Column(Integer, nullable=False)
    bitrate: float = Column(REAL, nullable=False)
    channels: int = Column(Integer, nullable=False)
    compilation: bool = Column(Boolean, nullable=False)
    comment: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    content_type: str = Column(String, nullable=False)
    copyright: str = Column(String, nullable=False)
    created_at: DateTime = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )
    date: str = Column(String, nullable=False)
    director: str = Column(String, nullable=False)
    directory: str = Column(String, nullable=False)
    duration: float = Column(REAL, nullable=False)
    disc_number: int = Column(Integer, nullable=False)
    disc_total: int = Column(Integer, nullable=False)
    filepath: str = Column(String, nullable=False)
    filesize: int = Column(Integer, nullable=False)
    genre: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)
    label: str = Column(String, nullable=False)
    lyrics: str = Column(Text, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    title: str = Column(String, nullable=False)
    track_id: str = Column(String(32), primary_key=True, nullable=False)
    track_number: int = Column(Integer, nullable=False)
    track_total: int = Column(Integer, nullable=False)
    updated_at: DateTime = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )
    year: int = Column(Integer, nullable=False)


class TrackModel(BaseModel):
    album: str
    album_id: str
    albumartist: str
    albumartist_id: str
    artist: str
    artist_id: str
    barcode: str
    bitdepth: int
    bitrate: float
    channels: int
    compilation: bool
    comment: str
    composer: str
    content_type: str
    copyright: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    date: str
    director: str
    directory: str
    duration: float
    disc_number: int
    disc_total: int
    filepath: str
    filesize: int
    genre: str
    isrc: str
    label: str
    lyrics: str
    samplerate: int
    title: str
    track_id: str
    track_number: int
    track_total: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    year: int


class TracksModel(BaseModel):
    album: str
    album_id: str
    artist: str
    artist_id: str
    duration: float
    title: str
    track_id: str


class TrackResponseModel(TrackModel):
    pass


class TracksResponseModel(BaseModel):
    tracks: list[TracksModel]
    total: int
