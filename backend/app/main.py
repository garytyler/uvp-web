from fastapi import FastAPI

from .api.routes import api_router
from .core.config import get_settings
from .core.db import register_db
from .core.middlewares import add_middlewares
from .core.redis import connect_redis, disconnect_redis


async def on_startup_event() -> None:
    await connect_redis()


async def on_shutdown_event() -> None:
    await disconnect_redis()


def get_app():
    app = FastAPI(
        debug=get_settings().DEBUG,
        title=get_settings().APP_TITLE,
        openapi_url="/api/openapi.json",
    )
    app.include_router(api_router)
    app.add_event_handler("startup", on_startup_event)
    app.add_event_handler("shutdown", on_shutdown_event)
    add_middlewares(app)
    register_db(app)
    return app


app = get_app()
