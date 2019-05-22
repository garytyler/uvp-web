import logging
import time
from importlib import import_module

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect

from .models import InteractorClient, MediaDisplayerClient

log = logging.getLogger(__name__)


class QueueConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.interactor_client, created = InteractorClient.objects.get_or_create(
            session_key=self.scope["session"].session_key
        )
        self.interactor_client.display_name = self.scope["session"]["display_name"]
        self.interactor_client.available = True
        self.interactor_client.save()
        self.queue_update()

    def queue_update(self):
        queue_objs = InteractorClient.objects.all()
        queue_list = [
            {
                "display_name": i.display_name,
                "session_key": i.session_key,
                "available": i.available,
            }
            for i in queue_objs
        ]
        self.send_json({"queue": queue_list})

    def receive_json(self, event):
        pass

    def disconnect(self, close_code):
        self.interactor_client.available = False
        self.interactor_client.save()


class InteractorConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.mediaplayer_channel_name = None
        self.accept()

    def receive_json(self, event):
        """Forward data from view operator to a single media player consumer"""
        if not self.mediaplayer_channel_name:
            mediaplayer_client = MediaDisplayerClient.objects.first()
            if mediaplayer_client:
                self.mediaplayer_channel_name = mediaplayer_client.channel_name
            else:
                log.info("NO MEDIA PLAYER CONNECTION FOUND")
                return

        log.info(event)
        async_to_sync(self.channel_layer.send)(
            self.mediaplayer_channel_name,
            {"type": "mediaplayer.sendview", "event": event},
        )

    def disconnect(self, close_code):
        pass


class MediaDisplayerClientConsumer(JsonWebsocketConsumer):

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
