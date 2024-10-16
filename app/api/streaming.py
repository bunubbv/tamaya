from fastapi import APIRouter, Header, status, Response, Depends
from core.depends import get_library_service

router = APIRouter(prefix='/api')

@router.get(
    '/streaming/{track_id}',
    summary="Streaming",
    responses={
        206: {},
        401: {},
        404: {},
        500: {},
    },
)
async def api_streaming(
    track_id: str,
    range: str = Header(None),
    service: get_library_service = Depends(),
) -> Response:

    content, headers = await service.streaming(track_id, range)
    return Response(
        content=content,
        headers=headers,
        status_code=status.HTTP_206_PARTIAL_CONTENT
    )
