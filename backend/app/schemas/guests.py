from app.models.guests import Guest
from pydantic import UUID4
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from .base import CustomPydanticBase


class GuestCreate(CustomPydanticBase):
    name: str
    feature_id: UUID4


class GuestUpdate(CustomPydanticBase):
    name: str
    feature_id: UUID4


Tortoise.init_models(["app.models.guests"], "models")

GuestOut = pydantic_model_creator(Guest, name="models.Guest")
