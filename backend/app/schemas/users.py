from typing import Optional

from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from app.models.users import User

from .base import CustomPydanticBase


class UserInCreate(CustomPydanticBase):
    email: str
    password: str
    is_active: bool = True


class UserDbCreate(CustomPydanticBase):
    email: str
    hashed_password: str
    is_active: bool = True


class UserInUpdate(CustomPydanticBase):
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]


class UserDbUpdate(CustomPydanticBase):
    email: Optional[str]
    hashed_password: Optional[str]
    is_active: Optional[bool]


Tortoise.init_models(["app.models.users"], "models")

UserOut = pydantic_model_creator(User, name="models.User", exclude=("hashed_password",))
