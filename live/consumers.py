import json
import logging

from channels.db import database_sync_to_async as db_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.sessions.backends.db import SessionStore
from django.core.cache import caches

from .models import Feature

log = logging.getLogger(__name__)


async def broadcast_feature_state(feature, groups):
    guest_queue_dict = []
    for session_key in feature.guest_queue:
        ss = SessionStore(session_key).load()
        guest_queue_dict.append(
            {"session_key": session_key, "guest_name": ss["guest_name"]}
        )
    for group_name in groups:
        await get_channel_layer().group_send(
            group_name,
            {
                "type": "layerevent.forward.to.client",
                "data": json.dumps(
                    {
                        "feature": {
                            "channel_name": feature.channel_name,
                            "title": feature.title,
                        },
                        "guest_queue": guest_queue_dict,
                    }
                ),
            },
        )


class GuestConsumer(AsyncWebsocketConsumer):
    cache = caches["default"]

    async def connect(self):
        """Initialize guest connections"""

        # Verify
        self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=self.scope["session"]["feature_slug"])
        )()
        if not self.feature and self.scope["session"]["guest_name"]:
            raise StopConsumer()

        # Add
        self.feature.guest_queue.append(self.scope["session"].session_key)
        for group_name in ["guests", self.scope["session"].session_key]:
            await self.channel_layer.group_add(group_name, self.channel_name)

        # Update
        await broadcast_feature_state(feature=self.feature, groups=["guests"])

        # Accept
        await self.accept()

    async def layerevent_forward_to_client(self, layer_event):
        await self.send(layer_event["data"])

    async def disconnect(self, close_code):
        self.feature.guest_queue.remove(self.scope["session"].session_key)


class PresenterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        feature_slug = self.scope["url_route"]["kwargs"]["feature_slug"]
        await db_sync_to_async(lambda: Feature.objects.get(slug=feature_slug).title)()
        await db_sync_to_async(
            lambda: Feature.objects.filter(slug=feature_slug).update(
                channel_name=self.channel_name
            )
        )()
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")
