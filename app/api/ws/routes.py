from fastapi.routing import APIRouter

from .endpoints import chat

ws_router = APIRouter()
ws_router.include_router(chat.router)
