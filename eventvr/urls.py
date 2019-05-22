from django.urls import path, re_path
from eventvr import views

app_name = "eventvr"

urlpatterns = [
    path("", views.join, name="join"),
    # re_path("^join/$", views.join, name="name"),
    re_path(r"^queue/$", views.queue, name="queue"),
    # re_path(r"^queue/(?P<interactor_name>[^/]+)/$", views.queue, name="queue"),
    # re_path(r"^interact/(?P<interactor_name>[^/]+)/$", views.interact, name="interact"),
    # re_path(r"^queue/$", views.queue, name="queue"),
    re_path(r"^interact/$", views.interact, name="interact"),
    re_path(r"^log_in/$", views.log_in, name="log_in"),
    re_path(r"^log_out/$", views.log_out, name="log_out"),
    re_path(r"^sign_up/$", views.sign_up, name="sign_up"),
]
