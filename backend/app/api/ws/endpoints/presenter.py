import asyncio

from app.api.dependencies.publish import publish_feature
from app.crud.features import crud_features
from app.crud.presenters import crud_presenters
from app.schemas.presenters import PresenterCreate
from app.services.broadcasting import broadcast
from fastapi import APIRouter, WebSocket, status

router = APIRouter()


@router.websocket("/presenter/{slug}")
async def on_connect(websocket: WebSocket) -> None:
    feature_slug = websocket.scope["path_params"].get("slug")
    feature = await crud_features.get_by_slug(slug=feature_slug)
    if not feature:
        return await websocket.close(code=status.HTTP_404_NOT_FOUND)
    presenter = await crud_presenters.create(
        obj_in=PresenterCreate(feature_id=feature.id)
    )
    await presenter.save()
    await websocket.accept()

    presenter_id = presenter.id
    await publish_feature(id=presenter_id)

    await run_loops(
        websocket=websocket,
        guest_channel=str(feature.guest_channel),
        presenter_channel=str(feature.presenter_channel),
    )

    deleted_count = await crud_presenters.delete(id=presenter_id)
    await publish_feature(id=feature.id)
    if not deleted_count:
        print("ERROR deleting presenter on websocket close")  # TODO
    await websocket.close()


async def loop_send_presenter_channel_to_client(websocket, presenter_channel):
    async with broadcast.subscribe(channel=presenter_channel) as subscriber:
        async for event in subscriber:
            await asyncio.sleep(0.01)
            await websocket.send_json(event.message)
        await asyncio.sleep(0.01)


async def loop_receive_from_client(websocket, guest_channel):
    async for message in websocket.iter_text():
        await asyncio.sleep(0.01)
    await asyncio.sleep(0.01)


async def run_loops(websocket, guest_channel, presenter_channel):
    tasks = [
        asyncio.create_task(
            loop_send_presenter_channel_to_client(
                websocket=websocket, presenter_channel=presenter_channel
            )
        ),
        asyncio.create_task(
            loop_receive_from_client(websocket=websocket, guest_channel=guest_channel)
        ),
    ]
    (tasks_done, tasks_pending) = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED
    )
    [task.result() for task in tasks_done]
    [task.cancel() for task in tasks_pending]
