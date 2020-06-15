from fastapi.routing import APIRouter

from .rest.routes import rest_router
from .ws.routes import ws_router

api_router = APIRouter()
api_router.include_router(rest_router, prefix="/api")
api_router.include_router(ws_router, prefix="/ws")
