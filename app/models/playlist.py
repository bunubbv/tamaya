from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from core.database import Base
from typing import Optional


class Playlist(Base):
    __tablename__ = 'playlists'

    playlist_id: str = Column(String, primary_key=True, nullable=False)
    playlist_title: str = Column(String, nullable=False)
    playlist_user_id: str = Column(String, ForeignKey('users.user_id'), nullable=False)
    created_at: DateTime = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at: DateTime = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    shared: bool = Column(Boolean, default=False, nullable=False)
    tracks = relationship("PlaylistData", backref="playlist", cascade="all, delete")


class PlaylistModel(BaseModel):
    playlist_id: str
    playlist_title: str
    playlist_user_id: str
    playlist_username: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    shared: bool


class PlaylistData(Base):
    __tablename__ = 'playlists_data'

    playlist_id: str = Column(
        String,
        ForeignKey('playlists.playlist_id', ondelete="CASCADE"),
        nullable=False,
    )
    track_id: str = Column(
        String,
        ForeignKey('tracks.track_id'),
        nullable=False,
    )
    added_at: DateTime = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    order: int = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        PrimaryKeyConstraint('playlist_id', 'track_id', 'added_at'),
    )


class PlaylistDataModel(BaseModel):
    playlist_id: str
    track_id: str
    added_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    order: int


class PlaylistTrackModel(BaseModel):
    album: str
    album_id: str
    artist: str
    artist_id: str
    duration: float
    title: str
    track_id: str


class PlaylistCreateModel(BaseModel):
    playlist_title: str
    shared: bool = False
    tracks: Optional[list[str]]


class PlaylistsResponseModel(BaseModel):
    playlists: list[PlaylistModel]
    total: int


class PlaylistResponseModel(PlaylistModel):
    tracks: list[PlaylistTrackModel]
