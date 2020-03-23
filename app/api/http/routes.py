from fastapi.routing import APIRouter

from .endpoints import broadcast

http_router = APIRouter()
http_router.include_router(broadcast.router)
