from fastapi.routing import APIRouter

from app.api.rest.routes import rest_router
from app.api.ws.routes import ws_router

api_router = APIRouter()


api_router.include_router(ws_router, prefix="/ws")
api_router.include_router(rest_router, prefix="/api")
