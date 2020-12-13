import uuid

from tortoise import fields

from app.models.guests import Guest
from app.models.presenters import Presenter
from app.models.users import User  # noqa F401

from .base import CustomTortoiseBase, TimestampMixin


class Feature(TimestampMixin, CustomTortoiseBase):
    id = fields.UUIDField(pk=True, read_only=True)
    interactor_channel_name = fields.UUIDField(default=uuid.uuid4, read_only=True)
    presenter_channel_name = fields.UUIDField(default=uuid.uuid4, read_only=True)
    title = fields.CharField(max_length=100, unique=True)
    slug = fields.CharField(index=True, required=True, unique=True, max_length=100)
    turn_duration = fields.IntField(required=True)
    guests = fields.ReverseRelation[Guest]
    presenters = fields.ReverseRelation[Presenter]
    user = fields.ForeignKeyField(
        "models.User", on_delete="CASCADE", related_name="features", null=True
    )

    class Meta:
        table = "features"

    class PydanticMeta:
        exclude = ("user",)
        allow_cycles = True
        max_recursion = 1

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.id)} name='{self.title}'>"

    def __str__(self):
        return self.__repr__()
