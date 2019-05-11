import eventvr.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter(eventvr.routing.websocket_urlpatterns)
        )
    }
)
