from fastapi.routing import APIRouter

from .endpoints import features, guests

http_router = APIRouter()
http_router.include_router(guests.router, tags=["guests"])
http_router.include_router(features.router, tags=["features"])
