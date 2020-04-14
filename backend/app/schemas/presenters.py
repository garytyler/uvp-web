from app.models.presenters import Presenter
from pydantic import UUID4
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from .base import CustomPydanticBase


class PresenterCreate(CustomPydanticBase):
    feature_id: UUID4


class PresenterUpdate(CustomPydanticBase):
    feature_id: UUID4


Tortoise.init_models(["app.models.presenters"], "models")

PresenterOut = pydantic_model_creator(Presenter, name="models.Presenter")
