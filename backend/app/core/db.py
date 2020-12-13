import os

from tortoise.contrib.fastapi import register_tortoise

from app.core.config import get_settings


def get_tortoise_config() -> dict:
    db_suffix = os.environ.get("DB_SUFFIX", "")
    return {
        "connections": {
            "default": f"{get_settings().DATABASE_URL}{db_suffix}",
        },
        "apps": {
            "models": {
                "models": [
                    "app.models.features",
                    "app.models.guests",
                    "app.models.presenters",
                    "app.models.users",
                ]
            },
        },
    }


TORTOISE_ORM = get_tortoise_config()


def register_db(app):
    register_tortoise(
        app,
        config=get_tortoise_config(),
        generate_schemas=True,
        add_exception_handlers=get_settings().DEBUG,
    )
