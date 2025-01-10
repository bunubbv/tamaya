from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from services.auth import AuthService


class CustomSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # 이거 너무 아닌 것 같음
        allowed = [
            "/api/auth/signup",
            "/api/auth/signin",
            "/api/auth/logout",
            "/api/auth/ping",
        ]

        if not request.url.path.startswith("/api") \
            or any(request.url.path.startswith(path) for path in allowed):

            return await call_next(request)

        session_id = request.cookies.get("session")
        if not session_id:
            response = Response(status_code=401)
            response.delete_cookie("session")
            return response

        username = AuthService.get_user_id(session_id)
        if not username:
            response = Response(status_code=401)
            response.delete_cookie("session")
            return response

        response = await call_next(request)
        return response
