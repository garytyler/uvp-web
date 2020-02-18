from django.urls import include, path
from rest_framework.routers import DefaultRouter

from seevr.live.api import views as api_views

router = DefaultRouter()
router.register(r"features", api_views.FeatureViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(r"guest/", api_views.GuestAPIView.as_view()),
    path(r"guest/<str:guest_id>/", api_views.GuestAPIView.as_view()),
    path(
        r"feature/<str:feature_slug>/guest/<str:guest_id>/",
        api_views.GuestAPIView.as_view(),
    ),
]
