from django.urls import re_path
from eventvr import consumers

websocket_urlpatterns = [
    re_path(r"^ws/queue", consumers.QueueConsumer),
    re_path(r"^ws/interactor", consumers.InteractorConsumer),
    re_path(r"^mediaplayer", consumers.MediaDisplayerConsumer),
]
