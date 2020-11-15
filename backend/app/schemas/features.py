from typing import Optional

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.features import Feature

from .base import CustomPydanticBase


class FeatureCreate(CustomPydanticBase):
    title: str
    slug: Optional[str]
    turn_duration: int = 180


class FeatureUpdate(CustomPydanticBase):
    title: str
    slug: Optional[str]
    turn_duration: int = 180


Tortoise.init_models(["app.models.features"], "models")

FeatureOut = pydantic_model_creator(Feature, name="models.Feature")
