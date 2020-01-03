from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter

import live.routing
from live import consumers

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(live.routing.websocket_urlpatterns)),
        "channel": ChannelNameRouter({"observer": consumers.StateObserverConsumer}),
    }
)
