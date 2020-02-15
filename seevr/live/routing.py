from django.urls import re_path

from seevr.live import consumers

websocket_urlpatterns = [
    re_path(r"^ws/guest_app/(?P<feature_slug>[^/]+)/$", consumers.GuestConsumer),
    # re_path(r"^ws/supervisor", consumers.SupervisorConsumer),
    re_path(r"^ws/presenter/(?P<feature_slug>[^/]+)/$", consumers.PresenterConsumer),
]
