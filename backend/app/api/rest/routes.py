from fastapi.routing import APIRouter

from .endpoints import features, guests

rest_router = APIRouter()
rest_router.include_router(guests.router, tags=["guests"])
rest_router.include_router(features.router, tags=["features"])
