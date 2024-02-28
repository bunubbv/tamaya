from core.convert_tools import *
from core.extract_tags import *
from core.tracks_service import *
from infra.path_handler import *
from infra.setup_logger import *

class LibraryHandler:
    @staticmethod
    async def create(path: str):
        track = TracksService(path)
        await track.create()

    @staticmethod
    async def update(path: str):
        track = TracksService(path)
        print("updated!")

    @staticmethod
    async def remove(path: str):
        track = TracksService(path)
        await track.remove()

    @staticmethod
    def images(image_id: str, size: int | str):
        image_dir = images_dir()
    
        if size == 'orig':
            for orig_image in image_dir.glob(f"{image_id}_orig*"):
                if orig_image.is_file(): return orig_image
        elif int(size) in IMAGE_SIZES:
            thumb_image = image_dir / f"{image_id}_{size}.{IMAGE_SUFFIX}"
            return thumb_image if thumb_image.is_file() else False
        else:
            return False