from fastapi.routing import APIRouter

from .http.routes import http_router
from .ws.routes import ws_router

router = APIRouter()
router.include_router(http_router, prefix="/api")
router.include_router(ws_router, prefix="/api/ws")
