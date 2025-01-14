import uuid
from typing import Any
from datetime import datetime, timezone
from fastapi import HTTPException, status
from core.database import NoResultFound
from models.user import UserModel, UserCreateModel, UserUpdateModel
from repos.user import UserRepo
from services.session import SessionService
from tools.convert_value import password_encode, password_verify


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def get_users(self) -> dict[str, list[dict[str, Any]] | int]:
        users, total = await self.repo.get_users()
        return { "users": users, "total": total }
    

    async def get_user(self, user_id: str) -> dict[str, Any]:
        try:
            user_data = await self.repo.get_user(user_id=user_id)
            return user_data
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        

    async def verify_user(self, email: str, password: str) -> dict[str, Any]:
        """
        Verify a user's email and password.

        Args:
            email (str): User's email address.
            password (str): Plain-text password provided by user.
        """

        user_data = await self.repo.get_user(email=email)

        if not password_verify(user_data.get('password', ''), password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user_data
        

    async def create_user(self, data: UserCreateModel) -> None:
        if await self.repo.get_user(email=data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        user_item = UserModel(
            user_id=str(uuid.uuid4()),
            email=data.email,
            username=data.username,
            password=password_encode(data.password),
        )

        await self.repo.create_user(user_item.model_dump())


    async def update_user(self, user_id: str, user_data: UserUpdateModel) -> None:
        check_user = await self.repo.get_user(user_id=user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.update_user(user_id, user_data.model_dump(exclude_unset=True))


    async def delete_user(self, user_id: str) -> None:
        check_user = await self.repo.get_user(user_id=user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        SessionService.delete_all_session(user_id)
        await self.repo.delete_user(user_id)


    async def post_signin(self, user_id: str) -> None:
        await self.repo.update_user(user_id, {"last_login": datetime.now(timezone.utc)})
