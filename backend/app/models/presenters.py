from __future__ import annotations

from tortoise import fields

from .base import CustomTortoiseBase, TimestampMixin


class Presenter(TimestampMixin, CustomTortoiseBase):
    id = fields.UUIDField(pk=True, read_only=True)
    feature = fields.ForeignKeyField(
        "models.Feature", on_delete="CASCADE", related_name="presenters", null=True
    )

    class Meta:
        table = "presenters"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.id)}>"

    def __str__(self):
        return self.__repr__()

    class PydanticMeta:
        exclude = (
            "created_at",
            "modified_at",
            # "feature",
        )
