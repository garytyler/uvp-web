from django.urls import include, path
from rest_framework.routers import DefaultRouter

from seevr.live.api.views import FeatureViewSet, GuestCreateAPIView, GuestListAPIView

router = DefaultRouter()
router.register(r"features", FeatureViewSet)
# router.register(r"guests", GuestViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "features/<slug:slug>/guests/", GuestListAPIView.as_view(), name="guest-list",
    ),
    path(
        "features/<slug:slug>/guest/",
        GuestCreateAPIView.as_view(),
        name="guest-create",
    ),
    # path(
    #     "features/<slug:slug>/answer/",
    #     GuestCreateAPIView.as_view(),
    #     name="guest-create",
    # ),
    # path("feature/<title:title>/", FeatureViewSet.as_view(), name="feature-detail"),
    # path(
    #     "questions/<slug:slug>/answer/",
    #     qv.AnswerCreateAPIView.as_view(),
    #     name="answer-create",
    # ),
    # path("answers/<int:pk>/", qv.AnswerRUDAPIView.as_view(), name="answer-detail",),
    # path("answers/<int:pk>/like/", qv.AnswerLikeAPIView.as_view(), name="answer-like")
]
