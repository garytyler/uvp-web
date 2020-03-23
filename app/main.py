from fastapi import FastAPI

from .api.routes import api_router
from .db.initialize import init_db
from .services.broadcast import connect_broadcaster, disconnect_broadcaster


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    app.add_event_handler("startup", connect_broadcaster)
    app.add_event_handler("shutdown", disconnect_broadcaster)
    init_db(app)
    return app


app = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
