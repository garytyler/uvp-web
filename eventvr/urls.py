from django.urls import path, re_path
from eventvr import views

app_name = "eventvr"

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^queue/(?P<visitorid>[^/]+)/$", views.queue, name="queue"),
    re_path(r"^log_in/$", views.log_in, name="log_in"),
    re_path(r"^log_out/$", views.log_out, name="log_out"),
    re_path(r"^sign_up/$", views.sign_up, name="sign_up"),
]
