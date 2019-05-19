import logging
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer

from .models import DisplayClient

log = logging.getLogger("django.server")


class QueueConsumer(JsonWebsocketConsumer):
    groups = ["queue"]

    def connect(self):
        self.accept()
        log.info("CONNECTED: queue_socket")

    def receive_json(self, event=None):
        pass

    def disconnect(self, close_code):
        pass


class ViewerConsumer(JsonWebsocketConsumer):
    groups = ["viewers"]

    def connect(self):
        # print(self.channel_name)
        self.accept()
        log.info("CONNECTED: viewersocket")

    def receive_json(self, event):
        display_client = DisplayClient.objects.first()

        log.info(display_client.channel_name)
        channel_layer = get_channel_layer()
        log.info(channel_layer)

        async_to_sync(channel_layer.send)(
            display_client.channel_name, {"type": "player.singleview", "event": event}
        )

        # async_to_sync(channel_layer.group_send)(
        #     "players", {"type": "player.groupview", "event": event}
        # )

    def disconnect(self, close_code):
        log.info("DISCONNECTED: viewersocket")
        pass


class MediaPlayerConsumer(JsonWebsocketConsumer):

    groups = ["players"]
    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    def incr_view(self, view):
        """Increment view values"""
        view["gn_euler"]["alpha"] += 0.1
        view["gn_euler"]["beta"] += 0.2
        view["gn_euler"]["gamma"] += 0.3

    def connect(self):
        DisplayClient(pk=1, channel_name=self.channel_name).save()
        log.info(DisplayClient.objects.first())

        log.info(f"MediaPlayer CONNECT: {self.channel_name}")
        self.accept()

    def receive_json(self, event=None):
        print(event)
        pass

    def player_singleview(self, single_event):
        self.send_json(single_event["event"])

    def player_view(self, eventdict):
        self.send_json(eventdict["event"])

    def disconnect(self, close_code):
        DisplayClient(pk=1, channel_name="").save()
        # TODO Notify all consumers of the media player disconnect with a signal
        log.info(f"MediaPlayer DISCONNECT: {self.channel_name}")
