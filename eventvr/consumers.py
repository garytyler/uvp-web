import logging
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer

from .models import MediaDisplayerClient

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


class InteractorConsumer(JsonWebsocketConsumer):
    def connect(self):
        mediaplayer_client = MediaDisplayerClient.objects.first()
        if mediaplayer_client:
            self.mediaplayer_channel_name = mediaplayer_client.channel_name
            self.accept()
            log.info("CONNECTED: viewersocket")
        else:
            log.info("NO MEDIA PLAYER CONNECTION FOUND")

    def receive_json(self, event):
        """Forward data from view operator to a single media player consumer"""
        log.info(event)
        async_to_sync(self.channel_layer.send)(
            self.mediaplayer_channel_name,
            {"type": "mediaplayer.sendview", "event": event},
        )

    def disconnect(self, close_code):
        log.info("DISCONNECTED: viewersocket")
        pass


class MediaDisplayerConsumer(JsonWebsocketConsumer):

    view = {"gn_euler": {"alpha": 10, "beta": 20, "gamma": 30}}

    def incr_view(self, view):
        """Increment view values"""
        view["gn_euler"]["alpha"] += 0.1
        view["gn_euler"]["beta"] += 0.2
        view["gn_euler"]["gamma"] += 0.3

    def connect(self):
        MediaDisplayerClient(pk=1, channel_name=self.channel_name).save()
        log.info(MediaDisplayerClient.objects.first())

        log.info(f"MediaPlayer CONNECT: {self.channel_name}")
        self.accept()

    def receive_json(self, event=None):
        print(event)
        pass

    def mediaplayer_sendview(self, eventdict):
        self.send_json(eventdict["event"])

    def disconnect(self, close_code):
        MediaDisplayerClient(pk=1, channel_name="").save()
        # TODO Notify all consumers of the media player disconnect with a signal
        log.info(f"MediaPlayer DISCONNECT: {self.channel_name}")
