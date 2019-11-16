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

from .models import Feature, MediaPlayer

log = logging.getLogger(__name__)


def get_feature_synchronously():
    try:
        feature = Feature.objects.get(pk=1)
    except Feature.DoesNotExist as e:
        feature = Feature(pk=1)
        log.debug("Create new Feature object")
        feature.save()
    return feature


@database_sync_to_async
def get_feature():
    return get_feature_synchronously()


@database_sync_to_async
def save_object(obj):
    obj.save()


@database_sync_to_async
def get_queue_state():
    feature = get_feature_synchronously()
    queue_state = []
    for session_key in feature.guest_queue:
        try:
            session_obj = Session.objects.get(pk=session_key)
        except Session.DoesNotExist:
            pass
        else:
            session_data = session_obj.get_decoded()
            session_data["session_key"] = session_key
            session_data.setdefault("channel_names", [])
            queue_state.append(session_data)
    return queue_state


@database_sync_to_async
def remove_from_guest_queue(session_key):
    log.info(f"REMOVE FROM GUEST QUEUE session_key={session_key}")
    feature = get_feature_synchronously()
    try:
        feature.guest_queue.remove(session_key)
    except ValueError as e:
        log.info(e)
    else:
        feature.save()


class SupervisorConsumer(AsyncJsonWebsocketConsumer):
    groups = ["supervisors"]

    async def connect(self):
        await self.accept()
        queue_state = await get_queue_state()
        await self.send_json({"queue_state": queue_state})

    async def layerevent_forward_to_client(self, layer_event):
        await self.send_json(layer_event["data"])

    async def receive_json(self, event):
        log.info(f"RECEIVED {event}")

        method = event["method"]
        if method == "remove_guest":
            await self.remove_guest(event["args"]["session_key"])

    async def remove_guest(self, session_key):
        feature = await get_feature()
        if session_key in feature.guest_queue:
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )


@database_sync_to_async
def add_guest_to_queue(session_key):
    feature = get_feature_synchronously()
    if session_key not in feature.guest_queue:
        feature.guest_queue.append(session_key)
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

        await self.accept()
        log.info(
            f"GUEST CONNECT session_key='{self.session.session_key}', channel_name='{self.channel_name}']"
        )

        # Add guest to queue if not already in it
        await add_guest_to_queue(session_key=self.session.session_key)

        await self.broadcast_queue_state(["guests", "supervisors"])

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
            await remove_from_guest_queue(session_key=self.session.session_key)

        for channel_name in ["guests", self.session.session_key]:
            await self.channel_layer.group_discard(channel_name, self.channel_name)

        await self.broadcast_queue_state(["guests", "supervisors"])

    async def layerevent_force_dequeue(self, layer_event):
        log.info(f"FORCE DEQUEUE session_key:'{self.session.session_key}'")
        close_code = layer_event["data"]["close_code"]
        self.session["channel_names"] = []
        await save_object(self.session)
        await self.shutdown_channel()
        await self.close(close_code)

    async def layerevent_forward_to_client(self, layer_event):
        await self.send_json(layer_event["data"])

    async def broadcast_queue_state(self, groups):
        queue_state = await get_queue_state()
        channel_layer = get_channel_layer()
        for group_name in groups:
            log.debug(f"BROADCAST queue state to '{group_name}'")
            await channel_layer.group_send(
                group_name,
                {
                    "type": "layerevent.forward.to.client",
                    "data": {"queue_state": queue_state},
                },
            )


@database_sync_to_async
def get_mediaplayer_channel_name():
    mediaplayer = MediaPlayer.objects.first()
    if mediaplayer:
        return mediaplayer.channel_name


class MotionConsumer(AsyncWebsocketConsumer):
    groups = ["motion"]

    async def connect(self):
        self.mediaplayer_channel_name = None

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
        self.mp_channel_name = await get_mediaplayer_channel_name()
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
        if self.session.session_key in feature.guest_queue:
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                self.session.session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )
        await self.broadcast_queue_state(["guests", "supervisors"])

    async def broadcast_queue_state(self, groups):
        queue_state = await get_queue_state()
        channel_layer = get_channel_layer()
        for group_name in groups:
            log.debug(f"BROADCAST queue state to '{group_name}'")
            await channel_layer.group_send(
                group_name,
                {
                    "type": "layerevent.forward.to.client",
                    "data": {"queue_state": queue_state},
                },
            )


def incr_view(view):
    """Increment view values"""
    view["gn_euler"]["alpha"] += 0.1
    view["gn_euler"]["beta"] += 0.2
    view["gn_euler"]["gamma"] += 0.3
    return view


@database_sync_to_async
def set_media_player_connection(channel_name):
    MediaPlayer(pk=1, channel_name=channel_name).save()
    log.info(f"MEDIAPLAYER CONNECT session_key:'{MediaPlayer.objects.first()}'")


class MediaPlayerConsumer(AsyncWebsocketConsumer):

    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    async def connect(self):
        await set_media_player_connection(channel_name=self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            "motion", {"type": "layerevent.new.mediaplayer.state", "data": {}}
        )

    async def receive(self, text_data=None, bytes_data=None):
        log.debug(f"{self.__class__.__name__} received text: {text_data}")
        log.debug(f"{self.__class__.__name__} received bytes: {bytes_data}")

    async def disconnect(self, close_code):
        await set_media_player_connection(channel_name=self.channel_name)
        log.info(f"MEDIAPLAYER DISCONNECT: {self.channel_name}")
        await self.channel_layer.group_send(
            "motion", {"type": "layerevent.new.mediaplayer.state", "data": {}}
        )

    async def layerevent_new_motion_state(self, event):
        """Forward event data that originated from guest client to media player client
        """
        await self.send(bytes_data=event["data"])
