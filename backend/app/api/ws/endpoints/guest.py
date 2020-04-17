import asyncio
import logging
from typing import Any

from app.api.dependencies.publish import publish_feature
from app.crud.features import crud_features
from app.services.broadcasting import broadcast
from fastapi import APIRouter, WebSocket, status
from starlette.endpoints import WebSocketEndpoint

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket_route("/guest/{slug}")
class WebsocketConsumer(WebSocketEndpoint):
    async def on_connect(self, websocket: WebSocket) -> None:
        # TODO Pass both feature id and guest id in route path and handle adding
        # guest to feature guest list here, and use another endpoint for non-guest
        # visitors.

        feature_slug = websocket.scope["path_params"].get("slug")
        feature = await crud_features.get_by_slug(slug=feature_slug)
        if not feature:
            return await websocket.close(code=status.HTTP_404_NOT_FOUND)
        await websocket.accept()
        feature_id = feature.id
        await publish_feature(id=feature_id)

        self.guest_channel = str(feature.guest_channel)

        self.guest_channel_subscriber_task = asyncio.create_task(
            self.loop_send_guest_channel_to_client(websocket=websocket)
        )

    async def loop_send_guest_channel_to_client(self, websocket):
        async with broadcast.subscribe(channel=self.guest_channel) as subscriber:
            async for event in subscriber:
                await asyncio.sleep(0.01)
                await websocket.send_text(event.message)
            await asyncio.sleep(0.01)

    async def on_receive(self, websocket: WebSocket, data: Any) -> None:
        await broadcast.publish(channel=self.guest_channel, message=data)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        for task in getattr(self, "tasks", []):
            task.cancel()
