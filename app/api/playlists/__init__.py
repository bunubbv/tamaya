from fastapi import APIRouter
from .playlist import router

playlists_router = APIRouter(
    prefix='/playlists',
    tags=['Playlists'],
)

playlists_router.include_router(playlist.router)