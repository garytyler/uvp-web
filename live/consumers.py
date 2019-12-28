import asyncio
import functools
import json
import logging
import threading
import time
from array import array
from importlib import import_module

from channels.db import database_sync_to_async as db_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings

from .caching import CachedListSet
from .models import Feature

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


async def broadcast_feature_state(feature, groups):
    SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
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
                "type": "forward.to.client",
                "data": {
                    "feature": {
                        "presenter_channel": feature.presenter_channel,
                        "title": feature.title,
                    },
                    "guest_queue": guest_queue_dict,
                },
            },
        )


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

        # Refresh queue state
        await self.channel_layer.send(
            self.feature.presenter_channel,
            {
                "type": "refresh_guest_queue_state",
                "message": {"feature_slug": self.feature.slug},
            },
        )
        # await self.channel_layer.send(
        #     "status-manager",
        #     {
        #         "type": "refresh_guest_queue_state",
        #         "message": {"feature_slug": self.feature.slug},
        #     },
        # )

    @channelmethod
    async def update_channel_status(self, collection_key):
        # await self.channel_layer.send(
        #     # "status-receiver",
        #     self.feature.presenter_channel,
        #     {
        #         "type": "receive_channel_status",
        #         "message": {
        #             "collection_key": collection_key,
        #             "session_key": self.scope["session"].session_key,
        #             "channel_name": self.channel_name,
        #         },
        #     },
        # )
        collection_key = collection_key
        session_key = self.scope["session"].session_key
        channel_name = self.channel_name
        log.debug(f"UPDATE STATUS - {session_key=}, {channel_name=}, {collection_key=}")
        CachedListSet(collection_key).append(f"{session_key}:{channel_name}")

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

        await self._run_status_watcher(feature_slug)

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")

    async def layerevent_new_motion_state(self, event):
        """Forward event data that originated from guest client to media player client
        """
        await self.send(bytes_data=event["data"])

    async def disconnect(self, close_code):
        self.feature.presenter_channel = None

    @channelmethod
    async def refresh_guest_queue_state(self, feature_slug):
        # await self._refresh_guest_queue_state(feature_slug)
        pass

    async def _run_status_watcher(self, feature_slug):
        def init_worker(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        loop = asyncio.new_event_loop()
        worker = threading.Thread(target=init_worker, args=(loop,))
        worker.setDaemon(True)
        worker.start()

        async def coro():
            while True:
                await self._refresh_guest_queue_state(feature_slug)
                await asyncio.sleep(4)

        loop.call_soon_threadsafe(lambda: asyncio.tasks.ensure_future(coro()))

    async def _refresh_guest_queue_state(self, feature_slug):
        begin = time.time()

        feature = self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=feature_slug)
        )()
        print(feature.member_channels)
        status_data = await self.get_group_status(
            group_name=feature.slug, num_channels=len(feature.member_channels)
        )

        # Update session keys
        feature.guest_queue.clear()
        feature.guest_queue.extend(status_data.keys())

        # Update session channels
        feature.member_channels.clear()
        _channels = []
        for sk in status_data.keys():
            _channels.extend(status_data[sk])
        feature.member_channels.extend(_channels)

        print("status_data", status_data)
        await self.broadcast_queue_data(feature.slug, status_data)

        # Finish
        time_spent = time.time() - begin
        log.info(f"REFRESHED GUEST QUEUE - {time_spent=}, {status_data=}")

    async def get_group_status(self, group_name, num_channels) -> dict:
        """
        - We use group_send instead of individual channel sends because:
          - Decoupling the observer pattern.
          - We can let timeouts handle stuck clients w/ minimal performance loss.
          - Letting timeouts handle stuck clients will help prevent race conditions
          that result in missing channels.
        - We will store channel names only to determiine when to exit listening
          during state updates.
        """
        # Initialize collection store
        collection_key = f"status-store:{group_name}"
        collection_store = CachedListSet(collection_key)
        collection_store.clear()

        # Request session status
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "update_channel_status",
                "message": {"collection_key": collection_key},
            },
        )

        # Wait for status responses
        timeout = time.time() + settings.GUEST_STATUS_PING_TIMEOUT
        while time.time() < timeout:
            await asyncio.sleep(0)
            if num_channels <= len(collection_store):
                break

        # Parse collected status data
        status: dict = {}
        for sk, cn in [i.split(":") for i in collection_store]:
            status.setdefault(sk, []).append(cn)

        collection_store.clear()

        return status

    async def broadcast_queue_data(self, group_name, status_data):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        queue_data = []
        for session_key, channel_names in status_data.items():
            ss = SessionStore(session_key).load()
            queue_data.append(
                {
                    "guest_name": ss["guest_name"],
                    "session_key": session_key,
                    "channel_names": channel_names,
                }
            )
        print(queue_data)
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "send_to_client",
                "message": {
                    "text_data": json.dumps(
                        {
                            "feature": {
                                "presenter_channel": self.feature.presenter_channel,
                                "title": self.feature.title,
                            },
                            "guest_queue": queue_data,
                        }
                    )
                },
            },
        )


class StatusReceiverConsumer(AsyncConsumer):
    groups = ["status-receiver"]

    @channelmethod
    async def receive_channel_status(self, collection_key, session_key, channel_name):
        log.debug(f"UPDATE STATUS - {session_key=}, {channel_name=}, {collection_key=}")
        CachedListSet(collection_key).append(f"{session_key}:{channel_name}")
