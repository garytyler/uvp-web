import logging
import queue
import time
from importlib import import_module

from asgiref.sync import async_to_sync
from channels.exceptions import ChannelFull
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect

from .models import Feature, MediaPlayer

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

log = logging.getLogger("django.channels.server")


def get_feature():
    return get_object_or_404(Feature, pk=1)


def get_queue_state():
    feature = get_feature()
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


def broadcast_queue_state(groups):
    queue_state = get_queue_state()
    channel_layer = get_channel_layer()
    for group_name in groups:
        log.info(f"BROADCAST QUEUE STATE to '{group_name}'")
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "layerrequest.forward.to.client",
                "data": {"queue_state": queue_state},
            },
        )


class SupervisorConsumer(JsonWebsocketConsumer):
    groups = ["supervisors"]

    def connect(self):
        self.accept()
        queue_state = get_queue_state()
        self.send_json({"queue_state": queue_state})

    def layerrequest_forward_to_client(self, channel_event):
        # print(channel_event)
        self.send_json(channel_event["data"])

    def receive_json(self, event):
        log.info(f"RECEIVED {event}")

        if event["method"] == "remove_guest":
            self.remove_guest(event["args"]["session_key"])

    def remove_guest(self, session_key):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            session_key,
            {"type": "layerrequest.supervisor.dequeue", "data": {"close_code": 4090}},
        )


class GuestConsumer(JsonWebsocketConsumer):
    def connect(self):
        """Initialize guest connections"""

        self.session = self.scope["session"]

        # Use session key as group name to handle multiple potential consumers per guest
        for group_name in ["guests", self.session.session_key]:
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

        feature = get_feature()
        if not self.session.session_key in feature.guest_queue:
            feature.guest_queue.append(self.session.session_key)
            feature.guest_history.append(self.session.session_key)
            feature.save()

        self.session.setdefault("channel_names", []).append(self.channel_name)
        self.session.save()
        self.accept()
        log.info(f"GUEST CONNECT channel_name: {self.channel_name}")

        broadcast_queue_state(["guests", "supervisors"])

    def layerrequest_forward_to_client(self, channel_event):
        self.send_json(channel_event["data"])

    def receive_json(self, event):
        """Handle dequeue request from guest

        #TODO Also use for ready confirmations in the future
        """
        pass

    def disconnect(self, close_code):
        self.shutdown_channel()
        log.info(
            f"GUEST DISCONNECT session_key: {self.session.session_key} channel_name:{self.channel_name}"
        )

    def shutdown_channel(self):
        """Handle persistence of guest state"""

        # Remove channel from session object
        if self.channel_name in self.session["channel_names"]:
            self.session["channel_names"].remove(self.channel_name)
            print(f"removed {self.channel_name} from {self.session['channel_names']}")
            self.session.save()
        else:
            log.error(f"channel_name '{self.channel_name}' not found in session object")

        # Dequeue guest if no more open channels
        if not self.session["channel_names"]:
            feature = get_feature()
            try:
                feature.guest_queue.remove(self.session.session_key)
            except ValueError as e:
                log.info(e)
            else:
                feature.save()

        for channel_name in ["guests", self.session.session_key]:
            async_to_sync(self.channel_layer.group_discard)(
                channel_name, self.channel_name
            )

        broadcast_queue_state(["guests", "supervisors"])

    def layerrequest_force_dequeue(self, channel_event):
        close_code = channel_event["data"]["close_code"]
        self.session["channel_names"] = []
        self.session.save()
        self.disconnect(close_code)
        self.close(close_code)

    def layerrequest_forward_to_client(self, channel_event):
        self.send_json(channel_event["data"])


class MotionConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.mediaplayer_channel_name = None

        self.session_key = self.scope["session"].session_key
        self.display_name = self.scope["session"]["display_name"]
        # TODO Verify session key match
        self.accept()

    def set_mediaplayer_channel_name(self):
        mediaplayer_client = MediaPlayer.objects.first()
        if mediaplayer_client:
            self.mediaplayer_channel_name = mediaplayer_client.channel_name

    def receive_json(self, motion_data):
        """Receive motion event data from guest client and forward it to media player consumer
        """
        if self.mediaplayer_channel_name:
            try:
                channel_event = {
                    "type": "layerrequest.forward.to.client",
                    "data": motion_data,
                }
                async_to_sync(self.channel_layer.send)(
                    self.mediaplayer_channel_name, channel_event
                )
            except ChannelFull:
                log.info("TODO: Handle ChannelFull")
                raise
            else:
                log.info(str(motion_data))
        else:
            mediaplayer_client = MediaPlayer.objects.first()
            if mediaplayer_client:
                self.mediaplayer_channel_name = mediaplayer_client.channel_name
                self.finished = True
            else:
                log.info("NO MEDIA PLAYER CONNECTED")

    def disconnect(self, close_code):
        # try:
        #     guest_query = Guest.objects.get(session_key=self.session_key)
        # except Guest.DoesNotExist:
        #     pass
        # else:
        #     guest_query.delete()
        # finally:
        #     async_to_sync(self.channel_layer.group_send)(
        #         "queue",
        #         {"type": "channel.request.next.guest.", "data": {"queue": queue_state}},
        #     )
        pass


def incr_view(view):
    """Increment view values"""
    view["gn_euler"]["alpha"] += 0.1
    view["gn_euler"]["beta"] += 0.2
    view["gn_euler"]["gamma"] += 0.3
    return view


class MediaDisplayerConsumer(JsonWebsocketConsumer):

    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    def connect(self):
        MediaPlayer(pk=1, channel_name=self.channel_name).save()
        log.info(MediaPlayer.objects.first())

        log.info(f"MediaPlayer CONNECT: {self.channel_name}")
        self.accept()

    def receive_json(self, event=None):
        log.info(event)
        pass

    def disconnect(self, close_code):
        MediaPlayer(pk=1, channel_name="").save()
        # TODO Notify all consumers of the media player disconnect with a signal
        log.info(f"MediaPlayer DISCONNECT: {self.channel_name}")

    def layerrequest_forward_to_client(self, channel_event):
        """Forward event data that originated from guest client to media player client
        """
        self.send_json(channel_event["data"])

    def send_motion_data(self, motion_data):
        self.send_json(motion_data)
