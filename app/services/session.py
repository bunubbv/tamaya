import uuid
from typing import Any
from diskcache import Cache
from core.config import Config


class SessionService:
    dc = Cache(Config.DATADIR)

    @classmethod
    def create_session(cls, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        cls.dc.set(session_id, user_id, expire=60 * 60 * 24 * 28) # 30 days
        return session_id
    

    @classmethod
    def delete_session(cls, session_id: str) -> None:
        if session_id: cls.dc.delete(session_id)
    

    @classmethod
    def delete_all_session(cls, user_id: str) -> None:
        for session_id in cls.dc.iterkeys():
            if cls.dc.get(session_id) == user_id:
                cls.dc.delete(session_id)
    

    @classmethod
    def get_user_id(cls, session_id: str) -> tuple[str | Any]:
        return cls.dc.get(session_id)
