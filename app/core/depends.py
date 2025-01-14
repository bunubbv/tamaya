from fastapi import Depends
from core.database import db_conn, AsyncGenerator
from services.library.library import LibraryService
from services.playlist import PlaylistService
from services.user import UserService
from repos.library import LibraryRepo
from repos.playlist import PlaylistRepo
from repos.user import UserRepo


async def get_library_repo() -> AsyncGenerator[LibraryRepo, None]:
    async with db_conn() as conn:
        yield LibraryRepo(conn)


async def get_library_service(
    repo: LibraryRepo = Depends(get_library_repo)
) -> LibraryService:
    return LibraryService(repo)


async def get_user_repo() -> AsyncGenerator[UserRepo, None]:
    async with db_conn() as conn:
        yield UserRepo(conn)


async def get_user_service(
    repo: UserRepo = Depends(get_user_repo)
) -> UserService:
    return UserService(repo)


async def get_playlist_repo() -> AsyncGenerator[PlaylistRepo, None]:
    async with db_conn() as conn:
        yield PlaylistRepo(conn)


async def get_playlist_service(
    repo: PlaylistRepo = Depends(get_playlist_repo)
) -> PlaylistService:
    return PlaylistService(repo)
