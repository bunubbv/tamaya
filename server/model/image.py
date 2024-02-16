from mutagen.aiff import AIFF
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.asf import ASF
from model.database import *
from tools.path import *
from PIL import Image
import imghdr
import io

image_resizes = [(64, 64), (128, 128), (300, 300), (500, 500)]

class ImageManagement:
    def __init__(self, path: str):
        if not PathTools.abs(path).is_dir():
            self.id = PathTools.get_md5_hash(path)
            self.str_path = path
            self.task_path = PathTools.abs(path)
            self.save_path = PathTools.abs('data') / 'images' / self.id
            self.suffix = PathTools.get_filename(path)[2].lower()
            self.image_data = None

    async def image_type(self):
        if self.suffix == '.mp3':
            self.image_data = await self.image_mp3()
        elif self.suffix == '.mp4' or self.suffix == '.m4a' or self.suffix == '.aac':
            self.image_data = await self.image_mp4()
        elif self.suffix == '.flac':
            self.image_data = await self.image_flac()
        elif self.suffix == '.alac':
            self.image_data = await self.image_alac()
        elif self.suffix == '.wma':
            self.image_data = await self.image_wma()
        elif self.suffix == '.aiff':
            self.image_data = await self.image_aiff()

        if self.image_data is not None:
            await self.image_process()
        else:
            return None

    async def image_process(self):
        suffix = imghdr.what(io.BytesIO(self.image_data))
        original_image = Image.open(io.BytesIO(self.image_data))
        original_image.save(self.save_path.as_posix() + f"_orig.{suffix}", format=suffix)

        for size in image_resizes:
            image = original_image.copy()
            image.thumbnail(size, Image.Resampling.LANCZOS)

            thumb_name = self.save_path.as_posix() + f"_{size[0]}_{size[1]}.{suffix}"
            image.save(thumb_name, format=suffix)

    async def image_mp3(self):
        audio = ID3(self.task_path)
        for tag in audio.values():
            if isinstance(tag, APIC):
                return tag.data 
        return None

    async def image_mp4(self):
        audio = MP4(self.task_path)
        covers = audio.get('covr')
        if covers:
            return covers[0].data
        return None

    async def image_flac(self):
        audio = FLAC(self.task_path)
        for picture in audio.pictures:
            if picture.type == 3:
                return picture.data
        return None

    async def image_alac(self):
        audio = MP4(self.task_path)
        covers = audio.tags.get('covr')
        if covers:
            return covers[0].data
        return None

    async def image_wma(self):
        audio = ASF(self.task_path)
        if 'WM/Picture' in audio.asf_tags:
            pictures = audio.asf_tags['WM/Picture']
            if pictures:
                return pictures[0].value.data
        return None

    async def image_aiff(self):
        audio = AIFF(self.task_path)
        if audio.tags is None:
            return None

        id3 = ID3(self.task_path)
        for tag in id3.values():
            if isinstance(tag, APIC):
                return tag.data
        return None