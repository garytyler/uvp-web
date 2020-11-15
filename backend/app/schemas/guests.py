from typing import Optional

from pydantic import UUID4
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from app.models.guests import Guest

from .base import CustomPydanticBase


class GuestUpdate(CustomPydanticBase):
    name: Optional[str]
    feature_id: Optional[UUID4]


Tortoise.init_models(["app.models.guests"], "models")

GuestCreate = pydantic_model_creator(
    Guest,
    name="GuestCreate",
    include=("feature_id", "name"),
)
GuestOut = pydantic_model_creator(
    Guest,
    name="GuestOut",
    include=("id", "feature_id", "name"),
)
