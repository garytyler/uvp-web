from datetime import timedelta
from typing import Optional

from pydantic import validator

from app.models.features import Feature
from app.services.features import feature_with_slug_exists, generate_unique_feature_slug
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from .base import CustomPydanticBase


class FeatureCreate(CustomPydanticBase):
    title: str
    slug: Optional[str]
    turn_duration: int = 180

    @validator("slug", always=True)
    @classmethod
    def validate_or_generate_slug(
        cls, slug, values,
    ):
        if not slug:
            slug = generate_unique_feature_slug(title=values["title"])
        elif feature_with_slug_exists(slug):
            raise ValueError(f"Feature with slug '{slug}' already exists")
        return slug


class FeatureUpdate(CustomPydanticBase):
    title: str
    slug: str
    turn_duration: timedelta


Tortoise.init_models(["app.models.features"], "models")

FeatureOut = pydantic_model_creator(Feature)
