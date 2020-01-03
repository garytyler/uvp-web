from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter

import live.routing
from live import consumers

application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "websocket": AuthMiddlewareStack(URLRouter(live.routing.websocket_urlpatterns)),
        "channel": ChannelNameRouter(
            {
                # "status-manager": consumers.StatusManagerConsumer,
                "status-receiver": consumers.StatusReceiverConsumer,
            }
        ),
    }
)
