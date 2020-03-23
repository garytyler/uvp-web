import uuid

from tortoise import fields, models

from .base import TimestampMixin


class Guest(TimestampMixin, models.Model):
    id = fields.data.UUIDField(default=uuid.uuid4, pk=True)
    session_key = fields.data.CharField(max_length=100, primary_key=True)
    name = fields.data.CharField(max_length=100)
    feature = fields.relational.ForeignKeyField(
        "models.Feature", on_delete="CASCADE", related_name="guests"
    )

    def __str__(self):
        return self.name
