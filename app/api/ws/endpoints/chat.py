import logging

from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from starlette.concurrency import run_until_first_complete

from app.services.broadcast import broadcast

log = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/guest")
async def connect(websocket: WebSocket):
    print("connect")
    await websocket.accept()
    await run_until_first_complete(
        (channel_receive, {"websocket": websocket}),
        (channel_send, {"websocket": websocket}),
    )


async def channel_receive(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="chatroom", message=message)


async def channel_send(websocket):
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)
