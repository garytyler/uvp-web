"""seevr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoseevr.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from seevr.views import IndexTemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("seevr.live.api.urls")),
    # path("", include("seevr.live.urls")),
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point"),
]
