from django.urls import path, re_path

from seevr.live import views

app_name = "live"

urlpatterns = [
    re_path(
        r"^(?P<feature_slug>(?!admin|ws|guest|supervise)[^/^]+)/$",
        views.guest_signup,
        name="guest_signup",
    ),
    re_path(
        r"^(?P<feature_slug>(?!admin|ws|guest|supervise)[^/^]+)/interact/$",
        views.guest_interact,
        name="guest_interact",
    ),
    path("supervise/", views.supervise, name="supervise"),
    path("guest/exit/", views.guest_exit, name="guest_exit"),
]
