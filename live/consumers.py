import logging

from channels.db import database_sync_to_async as db_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import caches

from .models import Feature

log = logging.getLogger(__name__)


class GuestConsumer(AsyncWebsocketConsumer):
    cache = caches["default"]

    async def connect(self):
        """Initialize guest connections"""

        # Verify guest
        self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=self.scope["session"]["feature_slug"])
        )()
        if not self.feature and self.scope["session"]["guest_name"]:
            raise StopConsumer()

        # Add guest
        self.feature.guest_queue.append(self.scope["session"].session_key)
        await self.channel_layer.group_add(
            self.scope["session"].session_key, self.channel_name
        )

        # Accept guest
        await self.accept()

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
