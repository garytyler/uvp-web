from django.urls import re_path

from live import consumers

websocket_urlpatterns = [
    re_path(r"^ws/guest", consumers.GuestConsumer),
    re_path(r"^ws/motion", consumers.MotionConsumer),
    re_path(r"^ws/supervisor", consumers.SupervisorConsumer),
    re_path(r"^feature/(?P<message>\w+)/$", consumers.FeatureConsumer),
]
