from fastapi import FastAPI

from .api.routes import api_router
from .core.db import register_db
from .core.middlewares import add_middlewares
from .services.broadcasting import connect_broadcaster, disconnect_broadcaster


async def on_startup_event() -> None:
    await connect_broadcaster()


async def on_shutdown_event() -> None:
    await disconnect_broadcaster()


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app.add_event_handler("startup", on_startup_event)
    app.add_event_handler("shutdown", on_shutdown_event)
    add_middlewares(app)
    register_db(app)
    return app


app = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
