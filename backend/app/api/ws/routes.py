from fastapi.routing import APIRouter

from .endpoints import guest, presenter

ws_router = APIRouter()
ws_router.include_router(guest.router)
ws_router.include_router(presenter.router)
