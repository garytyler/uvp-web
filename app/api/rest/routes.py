from fastapi.routing import APIRouter

from .endpoints import broadcast

rest_router = APIRouter()
rest_router.include_router(broadcast.router)
