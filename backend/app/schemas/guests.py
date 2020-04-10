from typing import Optional

from app.models.guests import Guest
from pydantic import UUID4
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from .base import CustomPydanticBase


class GuestCreateIn(CustomPydanticBase):
    name: str


class GuestCreateDb(CustomPydanticBase):
    name: str
    feature_id: UUID4


class GuestUpdateIn(CustomPydanticBase):
    name: str


class GuestUpdateDb(CustomPydanticBase):
    name: Optional[str]
    feature_id: Optional[UUID4]


Tortoise.init_models(["app.models.guests"], "models")

GuestOut = pydantic_model_creator(Guest, name="models.Guest")
