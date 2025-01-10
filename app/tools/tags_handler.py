from datetime import datetime
from tinytag import TinyTag, Image, Images
from typing import Any
from tools.path_handler import get_path, str_path
from tools.convert_value import (
    hash_str,
    get_mime,
    safe_list,
    convert_date,
    convert_artist,
)


def extract_tags(path: str) -> dict[str, Any]:
    path, real_path = str_path(path), get_path(path)
    
    try:
        tags = TinyTag.get(real_path)
        date, year = convert_date(tags.year)
        
        if tags.album:
            if tags.disc_total:
                album_id = hash_str(
                    tags.album,
                    tags.albumartist or '',
                    tags.disc_total,
                    str_path(get_path(path).parent),
                )
            else:
                album_id = hash_str(
                    tags.album,
                    tags.albumartist or '',
                    tags.track_total or 0,
                    str_path(get_path(path).parent),
                )
        else:
            album_id = hash_str(
                tags.artist,
                tags.albumartist or '',
                str_path(get_path(path).parent),
            )
        
        if tags.albumartist:
            albumartist_id = hash_str(tags.albumartist.lower())
        elif tags.artist:
            albumartist_id = hash_str(tags.artist.lower())


        track_dict = {
            'album': tags.album or '',
            'album_id': album_id,
            'albumartist': tags.albumartist or '',
            'albumartist_id': albumartist_id,
            'artist': tags.artist or '',
            'artist_id': hash_str(convert_artist(tags.artist.lower())) or '',
            'barcode': safe_list(tags.extra, 'barcode'),
            'bitdepth': tags.bitdepth or 0,
            'bitrate': tags.bitrate or 0.0,
            'channels': tags.channels or 0,
            'comment': tags.comment or '',
            'compilation': True if safe_list(tags.extra, 'compilation') else False,
            'composer': tags.composer or '',
            'content_type': get_mime(path),
            'copyright': safe_list(tags.extra, 'copyright'),
            'date': date,
            'director': safe_list(tags.extra, 'director'),
            'directory': str_path(get_path(path).parent),
            'duration': tags.duration or 0.0,
            'disc_number': tags.disc or 0,
            'disc_total': tags.disc_total or 0,
            'filepath': path,
            'filesize': tags.filesize or 0,
            'genre': tags.genre or '',
            'isrc': safe_list(tags.extra, 'isrc'),
            'label': safe_list(tags.extra, 'label'),
            'lyrics': safe_list(tags.extra, 'lyrics'),
            'samplerate': tags.samplerate or 0,
            'title': tags.title or '',
            'track_id': hash_str(path),
            'track_number': tags.track or 0,
            'track_total': tags.track_total or 0,
            'year': year,
        }

        return track_dict
    
    except Exception as e:
        return {}


def extract_artwork(path: str) -> bytes | None:
    try:
        tag: TinyTag = TinyTag.get(get_path(path), image=True)
        images: Images = tag.images
        cover_image: Image = images.front_cover

        return cover_image.data if cover_image is not None else None
    except:
        return None
