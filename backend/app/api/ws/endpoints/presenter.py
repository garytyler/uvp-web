import asyncio
from typing import Any

from fastapi import APIRouter, WebSocket, status

from app.api.dependencies.publish import publish_feature
from app.core.redis import ChannelReader, redis
from app.models.features import Feature
from app.models.presenters import Presenter
from app.schemas.presenters import PresenterCreate
from app.utils.endpoints import APIWebSocketEndpoint

router = APIRouter()


@router.websocket("/presenter/{slug}")
class PresenterWebSocket(APIWebSocketEndpoint):
    async def on_connect(self, websockets: WebSocket) -> None:
        feature_slug = websockets.scope["path_params"].get("slug")
        if not (feature := await Feature.get_or_none(slug=feature_slug)):
            return await websockets.close(code=status.HTTP_404_NOT_FOUND)
        presenter = await Presenter.create(
            **PresenterCreate(feature_id=feature.id).dict()
        )
        await presenter.save()
        await websockets.accept()
        self.presenter_ch_name = str(feature.presenter_channel_name)
        self.presenter_ch = (
            await redis.subscribe(str(feature.presenter_channel_name))
        )[0]
        await publish_feature(id=feature.id)
        self.worker_tasks = [
            asyncio.create_task(self.forward_channel_to_client(websockets=websockets))
        ]

    async def forward_channel_to_client(self, websockets):
        async for msg in ChannelReader(self.presenter_ch):
            await websockets.send_bytes(msg)

    async def on_receive(self, websockets: WebSocket, data: Any) -> None:
        await redis.publish(self.presenter_ch.name, data)

    async def on_disconnect(self, websockets: WebSocket, close_code: int) -> None:
        for task in getattr(self, "worker_tasks", []):
            task.cancel()
        presenter_ch = getattr(self, "presenter_ch")
        if presenter_ch:
            await redis.unsubscribe(presenter_ch)
