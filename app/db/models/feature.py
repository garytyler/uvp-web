import uuid
from datetime import timedelta

from slugify import slugify
from tortoise import fields, models

from .base import TimestampMixin


class Feature(TimestampMixin, models.Model):
    id = fields.data.UUIDField(default=uuid.uuid4, pk=True)
    title = fields.data.CharField(max_length=100)
    slug = fields.data.CharField(default="", max_length=100, editable=False)
    turn_duration = fields.data.TimeDeltaField(default=timedelta(minutes=2))

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        # TODO: Handle if object has been created and already has slug
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
