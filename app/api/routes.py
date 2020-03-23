from fastapi.routing import APIRouter

from app.api.http.routes import http_router
from app.api.ws.routes import ws_router

api_router = APIRouter()


api_router.include_router(ws_router, prefix="/api/ws")
api_router.include_router(http_router, prefix="/api")
