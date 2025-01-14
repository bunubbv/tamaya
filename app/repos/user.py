from typing import Any
from models import User
from core.database import (
    AsyncConnection, select, insert, update, delete, func, NoResultFound
)

class UserRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def get_users(self) -> dict[str, Any]:
        users_query = await self.conn.execute(select(User.__table__))
        users = users_query.mappings().all()

        total_query = await self.conn.execute(
            select(func.count()).select_from(User)
        )
        total_query = total_query.scalar_one()
        return users, total_query


    async def get_user(
        self,
        user_id: str | None = None,
        email: str | None = None
    ) -> dict[str, Any]:

        if user_id:
            db_query = await self.conn.execute(
                select(User.__table__).where(User.user_id == user_id)
            )
            user_item = db_query.mappings().first()
            return dict(user_item) if user_item else {}
        
        else:
            db_query = await self.conn.execute(
                select(User.__table__).where(User.email == email)
            )
            user_item = db_query.mappings().first()
            return dict(user_item) if user_item else {}


    async def create_user(self, user_data: dict[str, Any]) -> None:
        await self.conn.execute(
            insert(User).values(**user_data)
        )


    async def update_user(self, user_id: str, user_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(User).values(**user_data).where(User.user_id == user_id)
        )

    
    async def delete_user(self, user_id: str) -> None:
        await self.conn.execute(
            delete(User).where(User.user_id == user_id)
        )
