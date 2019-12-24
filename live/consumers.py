import asyncio
import json
import logging
from array import array

from channels.db import database_sync_to_async as db_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.sessions.models import Session

from .caching import CachedListSet
from .models import Feature

log = logging.getLogger(__name__)


async def broadcast_feature_state(feature, groups):
    SessionStore = Session.get_session_store_class()
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
                            "presenter_channel": feature.presenter_channel,
                            "title": feature.title,
                        },
                        "guest_queue": guest_queue_dict,
                    }
                ),
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

        # Add
        self.feature.guest_queue.append(self.scope["session"].session_key)

        self.scope["session"]["channel_names"] = []  # REMOVE !!!!!!!!!!!!!!!!!!!!

        self.scope["session"].setdefault("channel_names", []).append(self.channel_name)
        await db_sync_to_async(self.scope["session"].save)()
        await get_channel_layer().group_add(self.feature.slug, self.channel_name)

        # Accept
        await self.accept()

        await get_channel_layer().send(
            "status-manager",
            {
                "type": "refresh_guest_queue",
                "kwargs": {"feature_slug": self.feature.slug},
            },
        )
        # await self.broadcast_guest_queue()
        # # Update

    async def update_channel_status(self, event):
        async def _(collection_key):
            await self.reset_queue_member_expiry()
            await self.channel_layer.send(
                "status-receiver",
                {
                    "type": "receive_channel_status",
                    "kwargs": {
                        "collection_key": collection_key,
                        "session_key": self.scope["session"].session_key,
                        "channel_name": self.channel_name,
                    },
                },
            )

        await _(**event["kwargs"])

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

    async def layerevent_forward_to_client(self, layer_event):
        await self.send(layer_event["data"])

    async def disconnect(self, close_code):
        self.feature.guest_queue.remove(self.scope["session"].session_key)


class PresenterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        feature_slug = self.scope["url_route"]["kwargs"]["feature_slug"]
        self.feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=feature_slug)
        )()
        self.feature.presenter_channel = self.channel_name
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")

    async def layerevent_new_motion_state(self, event):
        """Forward event data that originated from guest client to media player client
        """
        await self.send(bytes_data=event["data"])

    async def disconnect(self, close_code):
        self.feature.presenter_channel = None


class StatusManagerConsumer(AsyncConsumer):
    SessionStore = Session.get_session_store_class()

    async def refresh_guest_queue(self, event):
        feature_slug = event["kwargs"]["feature_slug"]
        await self._update_and_get_guest_queue_member_status(feature_slug)

    async def _update_and_get_guest_queue_member_status(self, feature_slug):
        feature = await db_sync_to_async(
            lambda: Feature.objects.get(slug=feature_slug)
        )()
        curr_guest_queue = list(feature.guest_queue)

        # Get sessions and channels
        curr_session_stores = {sk: self.SessionStore(sk) for sk in curr_guest_queue}
        curr_channel_names = []
        for ss in curr_session_stores.values():
            await db_sync_to_async(ss.load)()
            curr_channel_names.extend(ss["channel_names"])

        # Initialize collection store
        collection_key = f"status-collection:{feature_slug}"
        collection_store = CachedListSet(collection_key)
        for i in collection_store:
            collection_store.remove(i)

        # Request status
        for channel_name in curr_channel_names:
            await get_channel_layer().send(
                channel_name,
                {
                    "type": "update_channel_status",
                    "kwargs": {"collection_key": collection_key},
                },
            )

        # Wait for status
        interval = 0.01
        num_loops = int(settings.GUEST_STATUS_PING_TIMEOUT / interval)
        num_channels = len(curr_channel_names)
        for _ in range(num_loops):
            await asyncio.sleep(interval)
            if num_channels <= len(collection_store):
                break

        # Parse collected status data
        member_status = {}
        for sk, cn in [i.split(":") for i in collection_store]:
            member_status.setdefault(sk, []).append(cn)

        # Update channel names in sessions
        to_disconnect = {}
        for sk, ss in curr_session_stores.items():
            ss.load()  # Potential channels added since last load call
            if sk in member_status.keys():
                for cn in ss["channel_names"]:
                    if cn in member_status[sk]:
                        continue
                    elif cn in curr_channel_names:  # Confirm not newly added
                        ss["channel_names"].remove(cn)
            else:
                to_disconnect.setdefault(ss["session_key"], [])
                for cn in ss["channel_names"]:
                    to_disconnect[sk].append(cn)
                ss["channel_names"] = []
            await db_sync_to_async(ss.save)()

        # Update session keys in guest queue
        for sk in curr_guest_queue:
            if sk not in member_status.keys():
                feature.guest_queue.remove(sk)

        return member_status


class StatusReceiverConsumer(AsyncConsumer):
    groups = ["status-receiver"]

    async def receive_channel_status(self, event):
        async def _(
            collection_key, session_key, channel_name,
        ):
            log.info(
                f"""
            receive_channel_status - {session_key=}, {channel_name=}, {collection_key=}
            """
            )
            CachedListSet(collection_key).append(f"{session_key}:{channel_name}")

        await _(**event["kwargs"])
