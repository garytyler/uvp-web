from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter

from backend.live import consumers
from backend.live.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
        "channel": ChannelNameRouter({"observer": consumers.StateObserverConsumer}),
    }
)
