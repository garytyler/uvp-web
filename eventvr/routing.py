from django.conf.urls import url

from eventvr import consumers

websocket_urlpatterns = [
    url(r"^ws/queue", consumers.QueueConsumer),
    url(r"^ws/viewer", consumers.ViewerConsumer),
    url(r"^mediaplayer", consumers.PlayerConsumer),
]
