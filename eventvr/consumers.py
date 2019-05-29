import array
import json
import logging
import queue
import time
from importlib import import_module

from asgiref.sync import async_to_sync
from channels.exceptions import ChannelFull
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect

from .models import Feature, MediaPlayer

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

# log = logging.getLogger("django.server")
log = logging.getLogger(__name__)
# log.info("asdfasdf")


"""
Exit codes:

4190 - Force dequeue by supervisor
4150 - Force dequeue by guest

"""


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
                "type": "layerevent.forward.to.client",
                "data": {"queue_state": queue_state},
            },
        )


class SupervisorConsumer(JsonWebsocketConsumer):
    groups = ["supervisors"]

    def connect(self):
        self.accept()
        queue_state = get_queue_state()
        self.send_json({"queue_state": queue_state})

    def layerevent_forward_to_client(self, layer_event):
        self.send_json(layer_event["data"])

    def receive_json(self, event):
        log.info(f"RECEIVED {event}")

        method = event["method"]
        if method == "remove_guest":
            self.remove_guest(event["args"]["session_key"])

    def remove_guest(self, session_key):
        feature = get_feature()
        if session_key in feature.guest_queue:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )
        # try:
        #     _session = Session.objects.get(pk=session_key)
        # except Session.DoesNotExist:
        #     pass
        # else:
        #     for key in ["display_name", "channel_names"]:
        #         try:
        #             _session.remove(key)
        #         except ValueError:
        #             pass


class GuestConsumer(JsonWebsocketConsumer):
    def connect(self):
        """Initialize guest connections"""

        self.session = self.scope["session"]

        # Use session key as group name to handle multiple potential consumers per guest
        for group_name in ["guests", self.session.session_key]:
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

        # Add this channel name to the guest's session object
        self.session.setdefault("channel_names", []).append(self.channel_name)
        self.session.save()
        self.accept()
        log.info(f"GUEST CONNECT channel_name: {self.channel_name}")

        # Add guest to queue if not already in it
        feature = get_feature()
        if not self.session.session_key in feature.guest_queue:
            feature.guest_queue.append(self.session.session_key)
            feature.save()

        broadcast_queue_state(["guests", "supervisors"])

    def receive_json(self, event):
        """Handle dequeue request from guest

        #TODO Also use for ready confirmations in the future
        """
        if event["method"] == "force_dequeue":
            # TODO Discard self from queue
            async_to_sync(self.channel_layer.group_send)(
                self.session.session_key,
                {"type": "layerevent.force.dequeue", "data": {"close_code": 4190}},
            )

    def disconnect(self, close_code):
        self.shutdown_channel()
        log.info(
            f"GUEST DISCONNECT session_key: {self.session.session_key} channel_name:{self.channel_name}"
        )

    def shutdown_channel(self):
        """Handle guest state persistence when only closing a single channel"""

        # Remove channel from session object
        if self.channel_name in self.session["channel_names"]:
            self.session["channel_names"].remove(self.channel_name)
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

    def layerevent_force_dequeue(self, layer_event):
        log.info(f"FORCE DEQUEUE {self.session.session_key}")
        close_code = layer_event["data"]["close_code"]
        self.session["channel_names"] = []
        self.session.save()
        self.shutdown_channel()
        self.close(close_code)

    def layerevent_forward_to_client(self, layer_event):
        self.send_json(layer_event["data"])


class MotionConsumer(WebsocketConsumer):
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

    def receive(self, text_data=None, bytes_data=None):
        """Receive motion event data from guest client and forward it to media player consumer
        """
        alpha, beta, gamma = array.array("d", bytes_data)
        print(alpha, beta, gamma)

        # if self.mediaplayer_channel_name:
        #     try:
        #         layer_event = {
        #             "type": "layerevent.forward.to.client",
        #             "data": motion_data,
        #         }
        #         async_to_sync(self.channel_layer.send)(
        #             self.mediaplayer_channel_name, layer_event
        #         )
        #     except ChannelFull:
        #         log.info("TODO: Handle ChannelFull")
        #         raise
        #     else:
        #         log.info(str(motion_data))
        # else:
        #     mediaplayer_client = MediaPlayer.objects.first()
        #     if mediaplayer_client:
        #         self.mediaplayer_channel_name = mediaplayer_client.channel_name
        #         self.finished = True
        #     else:
        #         log.info("NO MEDIA PLAYER CONNECTED")

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


class MediaDisplayerConsumer(WebsocketConsumer):

    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    def connect(self):
        MediaPlayer(pk=1, channel_name=self.channel_name).save()
        log.info(MediaPlayer.objects.first())

        log.info(f"MediaPlayer CONNECT: {self.channel_name}")
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        log.info(text_data)
        log.info(bytes_data)
        pass

    def disconnect(self, close_code):
        MediaPlayer(pk=1, channel_name="").save()
        log.info(f"MediaPlayer DISCONNECT: {self.channel_name}")

    def layerevent_forward_to_client(self, layer_event):
        """Forward event data that originated from guest client to media player client
        """
        self.send_json(layer_event["data"])

    def send_motion_data(self, motion_data):
        self.send_json(motion_data)
