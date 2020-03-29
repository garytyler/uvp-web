from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import settings


def add_middlewares(app):
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    if settings.HTTPS_REDIRECT is True:
        app.add_middleware(HTTPSRedirectMiddleware)
