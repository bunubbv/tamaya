from fastapi import APIRouter, Query, Depends
from models.track import TracksResponseModel, TrackResponseModel
from core.depends import get_library_service

router = APIRouter()

@router.get('/tracks', response_model=TracksResponseModel)
async def api_get_tracks(
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_library_service = Depends(),
) -> TracksResponseModel:
    
    return await service.get_tracks(start, end)


@router.get('/tracks/{track_id}', response_model=TrackResponseModel)
async def api_get_track(
    track_id: str,
    service: get_library_service = Depends(),
) -> TrackResponseModel:
    
    return await service.get_track(track_id)
