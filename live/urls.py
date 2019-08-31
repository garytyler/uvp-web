from django.urls import path

from live import views

app_name = "live"

urlpatterns = [
    path("", views.index, name="index"),
    # path("index/", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("interact/", views.interact, name="interact"),
    path("supervise/", views.supervise, name="supervise"),
    path("exit/", views.guest_exit, name="guest_exit"),
]
