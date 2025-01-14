from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.responses import FileResponse, StreamingResponse
from core.depends import get_library_repo, get_playlist_repo
from services.artwork import ArtworkService
from services.playlist import PlaylistService
from PIL import Image, ImageOps
import asyncio
import io

router = APIRouter()

@router.get('/artworks/{id}')
async def api_get_artwork(
    id: str,
    size: int = Query(300, ge=0),
    repo: get_library_repo = Depends(),
    play_repo: get_playlist_repo = Depends(),
) -> FileResponse:
    
    service = ArtworkService(repo)
    
    if not id.startswith('playlist_'):
        # Check if artwork is available in the filesystem ('artworks' directory).
        path = service.get_artwork_path(id, size)
        if path:
            return FileResponse(path)

        # Check if id (album or track) exists in library and extract if possible.
        data = await service.init_artwork(id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if size != 0:
            loop = asyncio.get_running_loop()
            img = await loop.run_in_executor(service.executor, Image.open, io.BytesIO(data))
            format = img.format.lower()

            await loop.run_in_executor(
                service.executor, img.thumbnail, [size, size], Image.Resampling.LANCZOS
            )

            buffer = io.BytesIO()
            img.save(buffer, format)
            buffer.seek(0)

            await loop.run_in_executor(
                service.executor, service.save_artwork, img, id, size, format
            )

            return StreamingResponse(buffer, media_type=f'image/{format}')
    else:
        id = id[9:] # exclude 'playlist_'

        # path = service.get_artwork_path(id, size)
        # if path:
        #     return FileResponse(path)

        play_service = PlaylistService(play_repo)
        playlist = await play_service.repo.get_playlist('playlist_' + id)
        if not playlist or not playlist.get('tracks'):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        tracks = playlist['tracks']
        track_ids = [track["track_id"] for track in tracks[:4]]

        images = []
        img_width = size
        img_height = size
        loop = asyncio.get_running_loop()

        for track_id in track_ids:
            track_path = service.get_artwork_path(track_id, size)
            if track_path:
                img = await loop.run_in_executor(service.executor, Image.open, track_path)
            else:
                track_data = await service.init_artwork(track_id)
                if not track_data:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                img = await loop.run_in_executor(service.executor, Image.open, io.BytesIO(track_data))

            # Resize the image
            img = await loop.run_in_executor(
                service.executor, ImageOps.fit, img, (img_width, img_height), Image.Resampling.BOX
            )
            images.append(img)

        num_images = len(images)

        if num_images == 3:
            images = [images[0], images[1], images[2], images[0]]
        elif num_images == 2:
            images = [images[0], images[1], images[1], images[0]]
        elif num_images == 1:
            buffer = io.BytesIO()
            images[0].save(buffer, format="jpeg", quality=90)
            buffer.seek(0)

            return StreamingResponse(buffer, media_type='image/jpeg')

        collage = Image.new('RGB', (img_width * 2, img_height * 2), (255, 255, 255))
        for index, img in enumerate(images[:4]):
            x_offset = (index % 2) * img_width
            y_offset = (index // 2) * img_height
            collage.paste(img, (x_offset, y_offset))

        buffer = io.BytesIO()
        collage_format = 'jpeg'
        collage.save(buffer, collage_format, quality=90)
        buffer.seek(0)

        await loop.run_in_executor(service.executor, service.save_artwork, collage, id, size, collage_format)
        return StreamingResponse(buffer, media_type=f'image/{collage_format}')