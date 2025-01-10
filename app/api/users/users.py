from fastapi import APIRouter, Query, Depends, Response, status, Request
from models.user import UserResponseModel, UsersResponseModel, UserUpdateModel
from models.playlist import PlaylistsResponseModel
from services.auth import AuthService
from core.depends import get_user_service, get_playlist_service

router = APIRouter()

@router.get('/',
    response_model=UsersResponseModel,
)
async def api_get_users(
    service: get_user_service = Depends(),
) -> UsersResponseModel:
    
    users = await service.get_users()
    return users


@router.get('/{user_id}',
    response_model=UserResponseModel,
)
async def api_get_user(
    user_id: str,
    service: get_user_service = Depends(),
) -> UserResponseModel:
    
    user = await service.get_user(user_id)
    return user


@router.put('/{user_id}')
async def api_update_user(
    user_id: str,
    user_data: UserUpdateModel,
    service: get_user_service = Depends()
) -> None:
    
    await service.update_user(user_id, user_data)
    return


@router.delete('/{user_id}')
async def api_delete_user(
    user_id: str,
    service: get_user_service = Depends()
) -> None:
    
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.get('/{user_id}/playlists', response_model=PlaylistsResponseModel)
# async def api_get_user_id_playlists(
#     user_id: str,
#     start: int = Query(1, ge=1),
#     end: int = Query(40, ge=1),
#     service: get_playlist_service = Depends(),
# ) -> PlaylistsResponseModel:
    
#     playlists = await service.get_playlists(user_id, start, end)
#     return playlists
