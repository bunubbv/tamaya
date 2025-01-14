import asyncio
from concurrent.futures import ThreadPoolExecutor
from core.database import db_conn
from core.logging import logs
from repos.library import LibraryRepo
from tools.tags_handler import extract_tags


class LibraryTask:
    semaphore = asyncio.Semaphore(5)

    def __init__(self, path: str) -> None:
        self.path = path
        self.tags = {}


    async def create_track(self) -> None:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            self.tags = await loop.run_in_executor(executor, extract_tags, self.path)

        if self.tags:
            async with self.semaphore:
                async with db_conn() as conn:
                    repo = LibraryRepo(conn)
                    await repo.insert_track(self.tags)
                    logs.debug(f"Track inserted: {self.tags.get('title')}")


    async def remove_track(self) -> None:
        async with self.semaphore:
            async with db_conn() as conn:
                repo = LibraryRepo(conn)
                await repo.delete_track(self.path)
                logs.debug(f"Track removed: {self.path}")


    async def update_track(self) -> None:
        async with self.semaphore:
            async with db_conn() as conn:
                repo = LibraryRepo(conn)
                await repo.delete_track(self.path)
                await self.create_track()

                logs.debug(f"Track recreated: {self.path}")
