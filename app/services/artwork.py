import asyncio
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from core.config import Config
from repos.library import LibraryRepo
from tools.path_handler import str_path, get_path, is_excluded_file, Path
from tools.tags_handler import extract_artwork

class ArtworkService:
    def __init__(self, repo: LibraryRepo) -> None:
        self.repo = repo
        self.executor = ThreadPoolExecutor(max_workers=20)


    def convert_hash(
        self,
        id: str,
        size: int
    ) -> Path:
        
        if size:
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
        

    def read_artwork_file(self, filepath: str) -> bytes:
        with open(filepath, 'rb') as f:
            return f.read()


    async def get_artwork(self, id: str, size: int) -> Path | None:
        if size != 0:
            thumb = self.convert_hash(id, size)
            return thumb if thumb.is_file() else None
        else:
            for original in Config.ARTWORKDIR.glob(str_path(self.convert_hash(id, size)) + '.*'):
                return original if original.is_file() else None


    async def init_artwork(self, id: str) -> bytes | None:
        try:
            data = await self.repo.get_item_path(id)
            artwork_path = get_path(data.get('filepath')).parent
        except:
            return None
    
        loop = asyncio.get_running_loop()
        for fs in artwork_path.iterdir():
            if fs.is_file() and fs.suffix.lower() in Config.ARTWORKTARGETS and not is_excluded_file(fs.name):
                return await loop.run_in_executor(self.executor, self.read_artwork_file, fs)

        return await loop.run_in_executor(
            self.executor, extract_artwork, data.get('filepath')
        )


    def save_artwork(
        self,
        data: Image.Image,
        id: str,
        size: int,
        type: str = Config.ARTWORKFORMAT
    ) -> None:
        
        img_name = str_path(
            get_path(self.convert_hash(id, size), create_dir=True),
            rel=False,
        )
        
        if not size:
            data.save(img_name, format=type)
        else:
            data.save(img_name, quality=Config.ARTWORKQUALITY)
