from tortoise.contrib.fastapi import register_tortoise

from app.core.config import get_settings

TORTOISE_ORM = {
    "connections": {"default": get_settings().DATABASE_URL},
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


def register_db(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        # db_url=get_settings().DATABASE_URL,
        # modules={"models": get_settings().TORTOISE_MODEL_MODULES},
        generate_schemas=True,
        add_exception_handlers=get_settings().DEBUG,
    )
