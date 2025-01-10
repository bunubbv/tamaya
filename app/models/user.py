from sqlalchemy import Column, String, DateTime, JSON
from enum import Enum
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from core.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id: str = Column(String, primary_key=True, nullable=False)
    email: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    last_login: DateTime = Column(DateTime, nullable=False)
    created_at: DateTime = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    role: str = Column(String, nullable=False)
    profile_img: str = Column(String, nullable=False)
    preferences: str = Column(JSON, nullable=False)


class UserRoleEnum(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    GUEST = 'guest'


class UserModel(BaseModel):
    user_id: str
    email: EmailStr
    username: str
    password: str
    last_login: datetime = Field(default_factory=lambda: datetime(1970, 1, 1, tzinfo=timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    role: UserRoleEnum = UserRoleEnum.USER
    profile_img: str = ''
    preferences: dict = Field(default_factory=dict)


class UserCreateModel(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdateModel(BaseModel):
    group: Optional[UserRoleEnum] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    profile_img: Optional[str] = None
    preferences: Optional[dict] = None


class UserSigninModel(BaseModel):
    email: EmailStr
    password: str


class UserResponseModel(UserModel):
    pass


class UsersResponseModel(BaseModel):
    users: list[UserResponseModel]
    total: int
