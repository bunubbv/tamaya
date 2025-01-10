import uuid
from datetime import datetime
from fastapi import HTTPException, status
from typing import Any
from core.database import NoResultFound
from models.user import UserModel, UserCreateModel, UserUpdateModel
from repos.user import UserRepo
from services.auth import AuthService


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def get_users(self) -> dict[str, list[dict[str, Any]] | int]:
        users, total = await self.repo.get_users()
        return {
            "users": users,
            "total": total
        }


    async def get_user(self, user_id: str) -> None:
        try:
            return await self.repo.get_user(user_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    async def check_credential(self, email: str, password: str) -> None:
        if not AuthService.password_verify(await self.repo.get_password(email), password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return await self.repo.get_user_id_from_email(email)
        

    async def user_login(self, email: str) -> None:
        user_id = await self.repo.get_user_id_from_email(email)
        if not user_id: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.update_user(user_id, {"last_login": datetime.now()})

    
    async def create_user(self, data: UserCreateModel) -> None:
        check_user = await self.repo.is_user_exist(data.email)
        if check_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        user_item = UserModel(
            user_id=str(uuid.uuid4()),
            email=data.email,
            username=data.username,
            password=AuthService.password_encode(data.password),
        )

        await self.repo.create_user(user_item.model_dump())


    async def update_user(self, user_id: str, user_data: UserUpdateModel) -> None:
        check_user = await self.repo.is_user_exist(user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.update_user(user_id, user_data.model_dump(exclude_unset=True))


    async def delete_user(self, user_id: str) -> None:
        check_user = await self.repo.is_user_exist(user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        AuthService.delete_all_session(user_id)
        await self.repo.delete_user(user_id)
