from app.core import settings
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def register_db(app):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.features", "app.models.guests"]},
        generate_schemas=True,
        add_exception_handlers=settings.DEBUG,
    )


def init_models():
    Tortoise.init_models(["__main__"], "models")
