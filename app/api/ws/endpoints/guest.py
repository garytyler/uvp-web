import asyncio
import logging
import typing

from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from starlette.concurrency import run_until_first_complete
from starlette.endpoints import WebSocketEndpoint

from app.services.broadcasting import broadcast

log = logging.getLogger(__name__)
router = APIRouter()


@router.websocket_route("/guest")
class GuestWebSocketApp(WebSocketEndpoint):
    # encoding = "text"

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        print("connected")
        self.channel_name = "chatroom"
        self.subscriber = broadcast.subscribe(channel=self.channel_name)
        await run_until_first_complete(
            (self.channel_receive, {"websocket": websocket}),
            (self.channel_send, {"websocket": websocket}),
        )

    async def channel_receive(self, websocket):
        print("channel_receive")
        async for message in websocket.iter_text():
            await broadcast.publish(channel="chatroom", message=message)
            await asyncio.sleep(0.01)

    async def channel_send(self, websocket):
        print("channel_send")
        async with broadcast.subscribe(channel="chatroom") as subscriber:
            async for event in subscriber:
                await asyncio.sleep(0.01)
                await websocket.send_text(event.message)
            await asyncio.sleep(0.01)

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_text(data)
