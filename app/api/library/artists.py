from fastapi import APIRouter, Query, Depends
from models.artist import ArtistsResponseModel, ArtistResponseModel
from core.depends import get_library_service

router = APIRouter()

@router.get('/artists', response_model=ArtistsResponseModel)
async def api_get_artists(
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_library_service = Depends(),
) -> ArtistsResponseModel:

    return await service.get_artists(start, end)


@router.get('/artists/{artist_id}', response_model=ArtistResponseModel)
async def api_get_artist(
    artist_id: str,
    service: get_library_service = Depends(),
) -> ArtistResponseModel:
    
    return await service.get_artist(artist_id)
