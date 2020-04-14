import asyncio
import logging

from app.api.dependencies.publish import publish_feature_by_obj
from app.crud.features import crud_features
from app.services.broadcasting import broadcast
from fastapi import APIRouter, WebSocket, status

log = logging.getLogger(__name__)
router = APIRouter()


@router.websocket_route("/guest/{slug}")
async def on_connect(websocket: WebSocket) -> None:
    feature_slug = websocket.scope["path_params"].get("slug")
    feature = await crud_features.get_by_slug(slug=feature_slug)
    if not feature:
        return await websocket.close(code=status.HTTP_404_NOT_FOUND)

    await websocket.accept()

    await publish_feature_by_obj(obj=feature)

    await run_loops(websocket=websocket, guest_channel=str(feature.guest_channel))
    await disconnect(websocket)


async def disconnect(websocket):
    await websocket.close()


async def loop_send_guest_channel_to_client(websocket, guest_channel):
    async with broadcast.subscribe(channel=guest_channel) as subscriber:
        async for event in subscriber:
            await asyncio.sleep(0.01)
            await websocket.send_text(event.message)
        await asyncio.sleep(0.01)


async def on_receive_from_client(websocket, guest_channel):
    async for message in websocket.iter_text():
        await broadcast.publish(channel=guest_channel, message=message)
        await asyncio.sleep(0.01)
    await asyncio.sleep(0.01)


async def run_loops(websocket, guest_channel):
    tasks = [
        asyncio.create_task(
            on_receive_from_client(websocket=websocket, guest_channel=guest_channel)
        ),
        asyncio.create_task(
            loop_send_guest_channel_to_client(
                websocket=websocket, guest_channel=guest_channel
            )
        ),
    ]
    (tasks_done, tasks_pending) = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED
    )
    [task.result() for task in tasks_done]
    [task.cancel() for task in tasks_pending]
