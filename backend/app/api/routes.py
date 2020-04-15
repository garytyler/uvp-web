from fastapi.routing import APIRouter

from .http.routes import http_router
from .ws.routes import ws_router

api_router = APIRouter()
api_router.include_router(http_router, prefix="/api")
api_router.include_router(ws_router, prefix="/ws")
