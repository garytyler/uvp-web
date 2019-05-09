from django.conf.urls import url
from eventvr import views

app_name = "eventvr"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^queue/(?P<visitorid>[^/]+)/$", views.queue, name="queue"),
    url(r"^log_in/$", views.log_in, name="log_in"),
    url(r"^log_out/$", views.log_out, name="log_out"),
    url(r"^sign_up/$", views.sign_up, name="sign_up"),
]
