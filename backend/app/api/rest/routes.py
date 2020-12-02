from fastapi.routing import APIRouter

from .endpoints import access, features, guests, users, utils

rest_router = APIRouter()
rest_router.include_router(guests.router, tags=["guests"])
rest_router.include_router(features.router, tags=["features"])
rest_router.include_router(access.router, tags=["access"])
rest_router.include_router(users.router, tags=["users"])
rest_router.include_router(utils.router, tags=["utils"])
