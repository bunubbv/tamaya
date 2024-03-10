from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter()

@router.get("/artists")
async def artists_list_api(num: int = Query(35, alias='num', gt=1, le=100)) -> list[dict]:
    try:
        artists_list = await LibraryTasks.get_artists(num=num)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err)

    if not artists_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return artists_list