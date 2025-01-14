from fastapi import Request, Response, APIRouter
from services.session import SessionService

router = APIRouter()

@router.post('/logout')
async def api_post_logout(request: Request, response: Response) -> None:
    session_id = request.cookies.get('session')
    
    if session_id:
        SessionService.delete_session(session_id)
        response.delete_cookie(key='session')
