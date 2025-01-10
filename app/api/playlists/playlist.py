from fastapi import APIRouter, Query, Depends, Response, Request, status
from models.playlist import PlaylistsResponseModel, PlaylistResponseModel, PlaylistCreateModel
from services.auth import AuthService
from core.depends import get_playlist_service, get_user_service

router = APIRouter()


@router.get('/', response_model=PlaylistsResponseModel)
async def api_get_user_playlists(
    request: Request,
    response: Response,
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_playlist_service = Depends(),
) -> PlaylistsResponseModel:

    playlists = await service.get_playlists(AuthService.get_user_id(request.cookies.get('session')), start, end)
    return playlists


@router.get('/{playlist_id}', response_model=PlaylistResponseModel)
async def api_get_playlist(
    playlist_id: str,
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_playlist_service = Depends(),
) -> PlaylistResponseModel:
    
    playlist = await service.get_playlist(playlist_id, start, end)
    return playlist


@router.delete('/{playlist_id}')
async def api_delete_playlist(
    playlist_id: str,
    service: get_playlist_service = Depends(),
) -> None:
    
    await service.delete_playlist(playlist_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/')
async def api_create_playlist(
    request: Request,
    response: Response,
    form: PlaylistCreateModel,
    service: get_playlist_service = Depends(),
) -> None:

    await service.create_playlist(form, AuthService.get_user_id(request.cookies.get('session')))


@router.patch('/{playlist_id}')
async def api_patch_playlist(

):
    pass
