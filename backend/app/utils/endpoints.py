from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket


class APIWebSocketEndpoint(WebSocketEndpoint):
    def __init__(self, websocket: WebSocket) -> None:
        super().__init__(
            scope=websocket.scope,
            receive=websocket.receive,
            send=websocket.send,
        )
