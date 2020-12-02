from tortoise import fields

from .base import CustomTortoiseBase, TimestampMixin


class User(TimestampMixin, CustomTortoiseBase):
    id = fields.UUIDField(pk=True, read_only=True)
    name = fields.CharField(index=True, max_length=100)
    email = fields.CharField(index=True, max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        table = "users"

    class PydanticMeta:
        ignore_extra = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.id)}>"

    def __str__(self):
        return self.__repr__()
