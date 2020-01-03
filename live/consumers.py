import functools
import logging
from array import array

from channels.db import database_sync_to_async as db_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer
from django.conf import settings

from live.app import caching, state
from live.models import Feature

log = logging.getLogger(__name__)


def channelmethod(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if kwargs:
            event = kwargs["event"]
        elif len(args) == 2:
            event = args[1]
        _self = args[0]
        return await func(_self, **event["message"])

    return wrapper


class GuestConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # Verify
        self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=self.scope["session"]["feature_slug"])
        )()
        if not self.feature and self.scope["session"]["guest_name"]:
            raise StopConsumer()

        # Accept
        await self.accept()

        # Add to queue
        self.feature.guest_queue.append(self.scope["session"].session_key)
        self.feature.member_channels.append(self.channel_name)
        await self.channel_layer.group_add(self.feature.slug, self.channel_name)

        # Broadcast state
        await state.broadcast_feature_state(self.feature)

    @channelmethod
    async def update_channel_status(self, collection_key):
        session_key = self.scope["session"].session_key
        channel_name = self.channel_name
        log.debug(f"UPDATE STATUS - {session_key=}, {channel_name=}, {collection_key=}")
        caching.CachedListSet(collection_key).append(f"{session_key}:{channel_name}")

    async def reset_queue_member_expiry(self):
        success = self.feature.guest_queue.reset_member_expiry(
            self.scope["session"].session_key
        )

        # TODO: Log uncessessful reset attempts
        if not success:
            raise RuntimeError("Error resetting queue member expiry")

    async def receive(self, text_data=None, bytes_data=None):
        """Receive motion event data from guest client and forward it to media player consumer
        """
        if bytes_data:
            await self.receive_bytes_data(data=bytes_data)
        else:
            await self.receive_text_data(data=text_data)

    async def receive_text_data(self, data):
        """
        TODO: Dictate which client has permission to send motion data

        When START is pressed, a request should be sent to the client's consumer, then:

        1. If 'feature.guest_channel_name' is set, notify that channel to stop sending
        motion data.

        2. Set 'feature.guest_channel_name' to the current consumer's channel_name.

        This will not guarentee prevention of receiving double motion states from
        multiple clients in the same session, but it should be good enough for now.
        """
        log.debug(f"{self.__class__.__name__} received text: {data}")

    async def receive_bytes_data(self, data):
        orientation_text = "{0:+f}{1:+f}{2:+f}".format(*array("d", data))
        log.debug(f"{self.__class__.__name__} received bytes: {orientation_text}")
        await self.channel_layer.send(
            self.feature.presenter_channel,
            {"type": "layerevent.new.motion.state", "data": data},
        )

    @channelmethod
    async def send_to_client(self, text_data=None, bytes_data=None, close=False):
        await self.send(text_data=text_data, bytes_data=bytes_data, close=close)

    async def disconnect(self, close_code):
        session_key = self.scope["session"].session_key
        self.feature.member_channels.remove(self.channel_name)
        self.feature.guest_queue.remove(session_key)


class PresenterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        feature_slug = self.scope["url_route"]["kwargs"]["feature_slug"]
        self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=feature_slug)
        )()
        self.feature.presenter_channel = self.channel_name

        await self.accept()

        if settings.USE_THREAD_BASED_FEATURE_OBSERVERS:
            await state.watch_feature_state_in_thread(feature_slug)

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")

    async def layerevent_new_motion_state(self, event):
        """Forward event data that originated from guest client to media player client
        """
        await self.send(bytes_data=event["data"])

    async def disconnect(self, close_code):
        self.feature.presenter_channel = None
        await db_sync_to_async(self.feature.save)()


class StateObserverConsumer(AsyncConsumer):
    @channelmethod
    async def run(self, feature_slugs=None):
        if settings.USE_THREAD_BASED_FEATURE_OBSERVERS:
            raise RuntimeError(
                "To run worker, disable 'USE_THREAD_BASED_FEATURE_OBSERVERS'."
            )
        await state.refresh_feature_states(feature_slugs)
