from django.conf.urls import url

from eventvr.consumers import QueueConsumer, PlayerConsumer

websocket_urlpatterns = [
    url(r"^queuews/(?P<visitorid>[^/]+)/$", QueueConsumer),
    url(r"^player", PlayerConsumer),
]

# url(r"^ws/chat/(?P<room_name>[^/]+)/$", consumers.ListConsumer)
# url(r"^ws/queue/(?P<id>[^/]+)/$", consumers.QueueConsumer)
