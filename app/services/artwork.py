import asyncio
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from core.config import Config
from repos.library import LibraryRepo
from tools.path_handler import str_path, get_path, is_excluded_file, Path
from tools.tags_handler import extract_artwork


class ArtworkService:
    def __init__(self, repo: LibraryRepo) -> None:
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.repo = repo


    def get_artwork_path(self, id: str, size: int) -> Path:
        if size != 0:
            thumb = self.get_hash_path(id, size)
            return thumb if thumb.is_file() else None
        else:
            for original in Config.ARTWORKDIR.glob(str_path(self.get_hash_path(id, size)) + '.*'):
                return original if original.is_file() else None


    def get_artwork_data(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()

    
    def get_hash_path(self, id: str, size: int) -> Path:
        """
        Generates a unique file path for an artwork hash.

        The path is organized into subdirectories based on the first 6 chars of the hash.
        Includes the size and file format if size is not 0.
        """

        if size != 0:
            return get_path(
                Config.ARTWORKDIR,
                f'{id[:2]}',
                f'{id[2:4]}',
                f'{id[4:6]}',
                f'{size}.{Config.ARTWORKFORMAT}'
            )
        else:
            return get_path(
                f'{id[:2]}',
                f'{id[2:4]}',
                f'{id[4:6]}',
                f'{size}'
            )


    async def init_artwork(self, id: str) -> bytes | None:
        # Playlist artwork is unnecessary to process.
        try:
            data = await self.repo.get_item_path(id)
            artwork_path = get_path(data).parent
        except:
            return None
    
        loop = asyncio.get_running_loop()
        for fs in artwork_path.iterdir():
            if fs.is_file() and fs.suffix.lower() in Config.ARTWORKTARGETS and not is_excluded_file(fs.name):
                return await loop.run_in_executor(self.executor, self.get_artwork_data, fs)

        return await loop.run_in_executor(
            self.executor, extract_artwork, data
        )


    def save_artwork(
        self,
        data: Image.Image,
        id: str,
        size: int,
        type: str = Config.ARTWORKFORMAT
    ) -> None:
        
        img_name = str_path(
            get_path(self.get_hash_path(id, size), create_dir=True),
            rel=False,
        )
        
        if not size:
            data.save(img_name, format=type)
        else:
            data.save(img_name, quality=Config.ARTWORKQUALITY)
