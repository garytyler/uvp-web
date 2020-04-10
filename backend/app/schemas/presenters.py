from app.models.presenters import Presenter
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from .base import CustomPydanticBase


class PresenterCreateDb(CustomPydanticBase):
    pass


class PresenterUpdateDb(CustomPydanticBase):
    pass


Tortoise.init_models(["app.models.presenters"], "models")

PresenterOut = pydantic_model_creator(Presenter, name="models.Presenter")
