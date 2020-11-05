from __future__ import annotations

from tortoise import fields

from .base import CustomTortoiseBase, TimestampMixin


class Guest(TimestampMixin, CustomTortoiseBase):
    id = fields.UUIDField(pk=True, read_only=True)
    name = fields.CharField(max_length=100)
    feature = fields.ForeignKeyField(
        "models.Feature", on_delete="CASCADE", related_name="guests"
    )

    class Meta:
        table = "guests"

    class PydanticMeta:
        allow_cycles = True
        max_recursion = 1
        orm_mode = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.id)} name='{self.name}'>"

    def __str__(self):
        return self.__repr__()
