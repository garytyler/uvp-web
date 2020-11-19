from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .config import get_settings


def add_middlewares(app):
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=get_settings().ALLOWED_HOSTS
    )
    app.add_middleware(SessionMiddleware, secret_key=get_settings().SECRET_KEY),
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
