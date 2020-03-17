from fastapi.routing import APIRouter

from .endpoints import home

rest_router = APIRouter()
rest_router.include_router(home.router)
