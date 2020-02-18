from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from seevr.live import state
from seevr.live.api.serializers import FeatureSerializer
from seevr.live.models import Feature
from seevr.live.utils import get_session_store


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    lookup_field = "slug"


class GuestAPIView(APIView):
    attr_keys = ["name"]

    def get(self, request):
        guest_name = request.session.get("name")
        request.session.save()
        return Response({"name": guest_name, "id": request.session.session_key})

    def post(self, request):
        guest_name = request.data.get("name")
        if not guest_name:
            return Response(
                "Guest name is required.", status=status.HTTP_400_BAD_REQUEST,
            )

        request.session["name"] = guest_name
        request.session.save()

        feature_slug = request.data.get("feature_slug")
        feature = Feature.objects.get(slug=feature_slug)
        async_to_sync(state.broadcast_feature_state)(feature)

        return Response(
            {"name": request.session["name"], "id": request.session.session_key}
        )

    def patch(self, request, feature_slug, guest_id):
        session_store = get_session_store(guest_id)

        for key in self.attr_keys:
            value = request.data.get(key)
            if value:
                session_store[key] = value
        session_store.save()

        feature = Feature.objects.get(slug=feature_slug)
        async_to_sync(state.broadcast_feature_state)(feature)

        return Response({**session_store.load(), "id": request.session.session_key})

    def delete(self, request, feature_slug, guest_id):
        feature = get_object_or_404(Feature, slug=feature_slug)

        if feature.guest_queue.remove(guest_id):
            error_code = status.HTTP_204_NO_CONTENT
            session_store = get_session_store(guest_id)
            session_store.flush()
            async_to_sync(state.broadcast_feature_state)(feature)

        else:
            error_code = status.HTTP_404_NOT_FOUND

        return Response(status=error_code,)
