from fastapi import APIRouter
from .auth import auth_router
from .library import library_router
from .playlists import playlists_router
from .server import server_router
from .sessions import sessions_router
from .users import users_router

api_router = APIRouter(prefix='/api')
api_router.include_router(auth_router)
api_router.include_router(library_router)
api_router.include_router(server_router)
api_router.include_router(sessions_router)
api_router.include_router(users_router)
api_router.include_router(playlists_router)
