import logging

from channels.db import database_sync_to_async as db_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import caches

from .models import Feature

log = logging.getLogger(__name__)


class GuestConsumer(AsyncWebsocketConsumer):
    cache = caches["default"]

    async def connect(self):
        """Initialize guest connections"""
        guest_name = self.scope["session"]["guest_name"]

        self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=self.scope["session"]["feature_slug"])
        )()
        assert guest_name and self.feature
        await self.feature.guest_queue.append(self.scope["session"])
        await self.accept()

    async def disconnect(self, close_code):
        await self.feature.guest_queue.remove(self.scope["session"])


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
