from django.urls import re_path
from eventvr import consumers

websocket_urlpatterns = [
    re_path(r"^ws/queue", consumers.QueueConsumer),
    re_path(r"^ws/viewer", consumers.ViewOperatorConsumer),
    re_path(r"^mediaplayer", consumers.MediaPlayerConsumer),
]
