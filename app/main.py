from fastapi import FastAPI

from .api.routes import router
from .core.db import register_db
from .core.events import create_shutdown_event_handler, create_startup_event_handler
from .core.middlewares import add_middlewares


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.add_event_handler("startup", create_startup_event_handler())
    app.add_event_handler("shutdown", create_shutdown_event_handler())
    add_middlewares(app)
    register_db(app)
    return app


app = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
