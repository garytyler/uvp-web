from tortoise import fields, models


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class CustomTortoiseBase(models.Model):
    class Meta:
        abstract = True
