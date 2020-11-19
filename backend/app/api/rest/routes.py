from fastapi.routing import APIRouter

from .endpoints import features, guests, login, users

rest_router = APIRouter()
rest_router.include_router(guests.router, tags=["guests"])
rest_router.include_router(features.router, tags=["features"])
rest_router.include_router(login.router, tags=["login"])
rest_router.include_router(users.router, tags=["users"])
