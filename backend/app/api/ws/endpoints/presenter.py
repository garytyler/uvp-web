import asyncio
from typing import Any

from app.api.dependencies.publish import publish_feature
from app.core.redis import ChannelReader, redis
from app.crud.features import crud_features
from app.crud.presenters import crud_presenters
from app.schemas.presenters import PresenterCreate
from app.utils.endpoints import APIWebSocketEndpoint
from fastapi import APIRouter, WebSocket, status

router = APIRouter()


@router.websocket("/guest/{slug}")
class PresenterWebSocket(APIWebSocketEndpoint):
    async def on_connect(self, ws: WebSocket) -> None:
        feature_slug = ws.scope["path_params"].get("slug")
        feature = await crud_features.get_by_slug(slug=feature_slug)
        if not feature:
            return await ws.close(code=status.HTTP_404_NOT_FOUND)
        presenter = await crud_presenters.create(
            obj_in=PresenterCreate(feature_id=feature.id)
        )
        await presenter.save()
        await ws.accept()
        self.presenter_ch = (await redis.subscribe(feature_slug))[0]
        await publish_feature(id=presenter.id)
        self.worker_tasks = [asyncio.create_task(self.forward_channel_to_client(ws=ws))]

    async def forward_channel_to_client(self, ws):
        async for msg in ChannelReader(self.presenter_ch):
            await ws.send_text(msg)

    async def on_receive(self, ws: WebSocket, data: Any) -> None:
        await redis.publish_text(self.feature_ch, data)

    async def on_disconnect(self, ws: WebSocket, close_code: int) -> None:
        for task in self.worker_tasks:
            task.cancel()
        await redis.unsubscribe(self.feature_ch)
