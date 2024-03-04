from fastapi import APIRouter, status, HTTPException
from core.services import *
from tools.convert_values import *

router = APIRouter()

@router.get("/tracks")
async def tracks_list_api(num: int = 28) -> list:
    limit = sanitize_num(num)
    tracks_list = await Library.get_tracks(num=limit)

    return tracks_list

@router.get("/tracks/{hash}")
async def tracks_api(hash: str) -> dict:
    tracks_path = await hash_to_track(hash)
    if not tracks_path: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    tracks_info = await Library.get_tracks(tracks_path)
    if not tracks_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return tracks_info