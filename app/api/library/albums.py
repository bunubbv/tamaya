from fastapi import APIRouter, Query, Depends
from models.album import AlbumsResponseModel, AlbumResponseModel
from core.depends import get_library_service

router = APIRouter()

@router.get('/albums', response_model=AlbumsResponseModel)
async def api_get_albums(
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_library_service = Depends(),
) -> AlbumsResponseModel:
    
    return await service.get_albums(start, end)


@router.get('/albums/{album_id}', response_model=AlbumResponseModel)
async def api_get_album(
    album_id: str,
    service: get_library_service = Depends(),
) -> AlbumResponseModel:
    
    return await service.get_album(album_id)
    