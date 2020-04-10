import asyncio
import json

from app.api.dependencies.publish import publish_feature_by_id
from app.crud.features import crud_features
from app.crud.presenters import crud_presenters
from app.models.presenters import Presenter
from app.schemas.features import FeatureOut
from app.services.broadcasting import broadcast
from fastapi import APIRouter, BackgroundTasks, WebSocket, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.websocket("/presenter/{slug}")
async def on_connect(websocket: WebSocket, background_tasks: BackgroundTasks) -> None:
    feature_slug = websocket.scope["path_params"].get("slug")
    feature = await crud_features.get_by_slug(slug=feature_slug)
    if not feature:
        return await websocket.close(code=status.HTTP_404_NOT_FOUND)

    presenter = await crud_presenters.create()

    await feature.save()
    await publish_feature_by_id(id=feature.id)
    await websocket.accept()

    feature_out = await FeatureOut.from_tortoise_orm(feature)
    data = {"action": "live/receiveFeature", "feature": jsonable_encoder(feature_out)}
    await websocket.send_json(json.dumps(data))

    await run_loops(
        websocket=websocket,
        guest_channel=str(feature.guest_channel),
        presenter_channel=str(feature.presenter_channel),
        feature=feature,
    )
    await disconnect(
        websocket=websocket,
        background_tasks=background_tasks,
        feature_id=feature.id,
        presenter_id=presenter.id,
    )


async def disconnect(websocket, background_tasks, feature_id, presenter_id):
    assert await Presenter.filter(id=presenter_id).delete()
    await publish_feature_by_id(id=feature_id)


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


async def run_loops(websocket, guest_channel, presenter_channel, feature):
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
    await publish_feature_by_id(id=feature.id)
    [task.result() for task in tasks_done]
    [task.cancel() for task in tasks_pending]
