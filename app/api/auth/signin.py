from fastapi import Depends, Response, APIRouter
from core.depends import get_user_service
from models.user import UserSigninModel
from services.session import SessionService

router = APIRouter()

@router.post("/signin")
async def api_post_signin(
    response: Response,
    form: UserSigninModel,
    service: get_user_service = Depends(),
) -> None:
    
    user_data = await service.verify_user(form.email, form.password)
    session_id = SessionService.create_session(user_data.get('user_id'))
    await service.post_signin(user_data.get('user_id'))

    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 28,
    )
