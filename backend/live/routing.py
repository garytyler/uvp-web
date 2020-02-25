from django.urls import re_path

from backend.live import consumers

websocket_urlpatterns = [
    re_path(r"^ws/guest/(?P<feature_slug>[^/]+)/$", consumers.GuestConsumer),
    # re_path(r"^ws/supervisor", consumers.SupervisorConsumer),
    re_path(r"^ws/presenter/(?P<feature_slug>[^/]+)/$", consumers.PresenterConsumer),
]
