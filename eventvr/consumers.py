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
        log.info(event)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "players", {"type": "player.view", "event": event}
        )

    def disconnect(self, close_code):
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
        self.accept()
        self.display_client = DisplayClient(pk=1)
        self.display_client.channel_name = self.channel_name
        self.display_client.save()
        # log.info("CONNECTED: player")

    def receive_json(self, event=None):
        pass

    def player_view(self, group_event):
        self.send_json(group_event["event"])

    def disconnect(self, close_code):
        # self.display_client.channel_name.set(None)
        pass
