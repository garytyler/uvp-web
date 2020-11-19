from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from app.models.users import User

from .base import CustomPydanticBase


class UserIn(CustomPydanticBase):
    email: str
    password: str


class UserCreate(CustomPydanticBase):
    email: str
    hashed_password: str
    is_active: bool = True


class UserUpdate(CustomPydanticBase):
    email: str
    hashed_password: str
    is_active: bool


Tortoise.init_models(["app.models.users"], "models")
UserOut = pydantic_model_creator(
    User,
    name="models.User",
    exclude_readonly=True,
)
