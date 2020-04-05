from fastapi.routing import APIRouter

from .endpoints import guest

ws_router = APIRouter()
ws_router.include_router(guest.router)
