import array
import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
)
from channels.layers import get_channel_layer
from django.contrib.sessions.models import Session

from .guests import SessionQueueInterface
from .models import Feature

log = logging.getLogger(__name__)


def get_feature_synchronously():
    feature, created = Feature.objects.get_or_create(pk=1)
    if created:
        log.debug("Create new Feature object")
    return feature


@database_sync_to_async
def get_feature():
    return get_feature_synchronously()


@database_sync_to_async
def save_object(obj):
    obj.save()


@database_sync_to_async
def get_current_guests_state():
    feature = get_feature_synchronously()
    current_guests_state = []
    for session_key in feature.current_guests:
        try:
            session_obj = Session.objects.get(pk=session_key)
        except Session.DoesNotExist:
            pass
        else:
            session_data = session_obj.get_decoded()
            session_data["session_key"] = session_key
            session_data.setdefault("channel_names", [])
            current_guests_state.append(session_data)
    return current_guests_state


@database_sync_to_async
def remove_from_current_guests(session_key):
    log.info(f"REMOVE FROM GUEST QUEUE session_key={session_key}")
    feature = get_feature_synchronously()
    try:
        feature.current_guests.remove(session_key)
    except ValueError as e:
        log.info(e)
    else:
        feature.save()


class SupervisorConsumer(AsyncJsonWebsocketConsumer):
    groups = ["supervisors"]

    async def connect(self):
        await self.accept()
        current_guests_state = await get_current_guests_state()
        await self.send_json({"current_guests_state": current_guests_state})

    async def layerevent_forward_to_client(self, layer_event):
        await self.send_json(layer_event["data"])

    async def receive_json(self, event):
        log.info(f"RECEIVED {event}")

        method = event["method"]
        if method == "remove_guest":
            await self.remove_guest(event["args"]["session_key"])

    async def remove_guest(self, session_key):
        feature = await get_feature()
        if session_key in feature.current_guests:
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )


@database_sync_to_async
def add_guest_to_queue(session_key):
    feature = get_feature_synchronously()
    if session_key not in feature.current_guests:
        feature.current_guests.append(session_key)
        feature.save()


@database_sync_to_async
def append_to_session_channel_names(session, channel_name):
    session.setdefault("channel_names", [channel_name])
    session.save()


@database_sync_to_async
def remove_from_session_channel_names(session, channel_name):
    session["channel_names"].remove(channel_name)
    session.save()


class GuestConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """Initialize guest connections"""

        self.session = self.scope["session"]

        # Use session key as group name to handle multiple potential consumers per guest
        for group_name in ["guests", self.session.session_key]:
            await self.channel_layer.group_add(group_name, self.channel_name)

        # Add this channel name to the guest's session object
        await append_to_session_channel_names(
            session=self.session, channel_name=self.channel_name
        )
        feature = await get_feature()
        guest_queue = SessionQueueInterface(queue_key=feature.pk)
        guest_queue.add(session_key=self.scope["session"].session_key)
        await self.accept()
        log.info(
            f"GUEST CONNECT session_key='{self.session.session_key}', channel_name='{self.channel_name}']"
        )

        # Add guest to queue if not already in it
        await add_guest_to_queue(session_key=self.session.session_key)

        await self.broadcast_current_guests_state(["guests", "supervisors"])

    async def receive_json(self, event):
        """Handle dequeue request from guest

        #TODO Also use for ready confirmations in the future
        """
        if event["method"] == "force_dequeue":
            # TODO Discard self from queue
            await self.channel_layer.group_send(
                self.session.session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )

    async def disconnect(self, close_code):
        await self.shutdown_channel()
        log.info(f"GUEST DISCONNECT channel_name='{self.channel_name}'")

    async def shutdown_channel(self):
        """Handle guest state persistence when only closing a single channel"""

        # Remove channel from session object
        if self.channel_name in self.session["channel_names"]:
            await remove_from_session_channel_names(
                session=self.session, channel_name=self.channel_name
            )
        else:
            log.info(f"channel_name '{self.channel_name}' not found in session object")

        # Dequeue guest if no more open channels
        if not self.session["channel_names"]:
            await remove_from_current_guests(session_key=self.session.session_key)

        for channel_name in ["guests", self.session.session_key]:
            await self.channel_layer.group_discard(channel_name, self.channel_name)

        await self.broadcast_current_guests_state(["guests", "supervisors"])

    async def layerevent_force_dequeue(self, layer_event):
        log.info(f"FORCE DEQUEUE session_key:'{self.session.session_key}'")
        close_code = layer_event["data"]["close_code"]
        self.session["channel_names"] = []
        await save_object(self.session)
        await self.shutdown_channel()
        await self.close(close_code)

    async def layerevent_forward_to_client(self, layer_event):
        await self.send_json(layer_event["data"])

    async def broadcast_current_guests_state(self, groups):
        current_guests_state = await get_current_guests_state()
        channel_layer = get_channel_layer()
        for group_name in groups:
            log.debug(f"BROADCAST queue state to '{group_name}'")
            await channel_layer.group_send(
                group_name,
                {
                    "type": "layerevent.forward.to.client",
                    "data": {"current_guests_state": current_guests_state},
                },
            )


@database_sync_to_async
def get_feature_channel_name():
    feature = Feature.objects.first()
    if feature:
        return feature.channel_name


class MotionConsumer(AsyncWebsocketConsumer):
    groups = ["motion"]

    async def connect(self):
        self.feature_channel_name = None

        self.session = self.scope["session"]
        self.display_name = self.session["display_name"]
        # TODO Verify session key match

        log.info(
            f"MOTION CONNECT session_key='({self.session.session_key}' channel_name='{self.channel_name}'"
        )
        await self.accept()
        await self.send_mediaplayer_state()

    async def layerevent_new_mediaplayer_state(self, content):
        await self.send_mediaplayer_state()

    async def send_mediaplayer_state(self):
        self.mp_channel_name = await get_feature_channel_name()
        if self.mp_channel_name:
            args = {"fps": 30, "allowed_time": 60, "media_title": "Mock Media Message"}
            await self.send(json.dumps({"method": "permission_granted", "args": args}))
        else:
            args = {"reason": "Media player not available."}
            await self.send(json.dumps({"method": "permission_denied", "args": args}))

    async def receive(self, text_data=None, bytes_data=None):
        """Receive motion event data from guest client and forward it to media player consumer
        """
        log.debug(
            f"{self.__class__.__name__} received: {'{0:+f}{1:+f}{2:+f}'.format(*array.array('d', bytes_data))}"
        )
        await self.channel_layer.send(
            self.mp_channel_name,
            {"type": "layerevent.new.motion.state", "data": bytes_data},
        )

    async def disconnect(self, close_code):
        """Broadcast a request for any open guest channels to dequeue themselves, then
        remove remaning channel names from associated session object, then broadcast a
        queue change to initiate another guest interactor
        """
        feature = await get_feature()
        if self.session.session_key in feature.current_guests:
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                self.session.session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )
        await self.broadcast_current_guests_state(["guests", "supervisors"])

    async def broadcast_current_guests_state(self, groups):
        current_guests_state = await get_current_guests_state()
        channel_layer = get_channel_layer()
        for group_name in groups:
            log.debug(f"BROADCAST queue state to '{group_name}'")
            await channel_layer.group_send(
                group_name,
                {
                    "type": "layerevent.forward.to.client",
                    "data": {"current_guests_state": current_guests_state},
                },
            )


def incr_view(view):
    """Increment view values"""
    view["gn_euler"]["alpha"] += 0.1
    view["gn_euler"]["beta"] += 0.2
    view["gn_euler"]["gamma"] += 0.3
    return view


class MediaPlayerConsumer(AsyncWebsocketConsumer):

    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    async def connect(self):
        print(self.scope["session"].session_key)
        await self.set_feature_channel_name(channel_name=self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            "motion", {"type": "layerevent.new.mediaplayer.state", "data": {}}
        )

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")

    async def disconnect(self, close_code):
        await self.set_feature_channel_name(channel_name=self.channel_name)
        await self.channel_layer.group_send(
            "motion", {"type": "layerevent.new.mediaplayer.state", "data": {}}
        )

    async def layerevent_new_motion_state(self, event):
        """Forward event data that originated from guest client to media player client
        """
        await self.send(bytes_data=event["data"])

    @database_sync_to_async
    def set_feature_channel_name(self, channel_name):
        feature = Feature(pk=1)
        feature.channel_name = channel_name
        feature.save()
