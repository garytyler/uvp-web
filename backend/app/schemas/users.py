from typing import Optional

from pydantic import EmailStr
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from app.models.users import User

from .base import CustomPydanticBase


class UserInCreate(CustomPydanticBase):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True


class UserDbCreate(CustomPydanticBase):
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True


class UserInUpdate(CustomPydanticBase):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]


class UserDbUpdate(CustomPydanticBase):
    name: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    is_active: Optional[bool]


Tortoise.init_models(["app.models.users"], "models")

UserOut = pydantic_model_creator(
    User,
    name="models.User",
    exclude=("hashed_password", "features"),
)
