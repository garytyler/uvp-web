from app.core.config import settings
from tortoise.contrib.fastapi import register_tortoise


def register_db(app):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": settings.TORTOISE_MODEL_MODULES},
        generate_schemas=True,
        add_exception_handlers=settings.DEBUG,
    )
