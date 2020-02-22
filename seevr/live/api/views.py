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

    def get(self, request, feature_slug):
        """Get guest from a feature guest queue"""
        feature = get_object_or_404(Feature, slug=feature_slug)
        sk = request.session.session_key

        if sk and sk in feature.guest_queue:
            guest_name = request.session.get("name")
            if guest_name:
                return Response({"name": guest_name, "id": sk})
            else:
                feature.guest_queue.remove(sk)
                async_to_sync(state.broadcast_feature_state)(feature)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, feature_slug):
        """Add guest to feature guest queue"""
        feature = get_object_or_404(Feature, slug=feature_slug)

        guest_name = request.data.get("name")
        if not guest_name:
            return Response(
                "Guest name is required.", status=status.HTTP_400_BAD_REQUEST,
            )

        request.session["name"] = guest_name
        request.session.save()

        feature.guest_queue.append(request.session.session_key)
        async_to_sync(state.broadcast_feature_state)(feature)

        return Response(
            {"name": request.session["name"], "id": request.session.session_key}
        )

    def patch(self, request, feature_slug, guest_id):
        """Update guest profile"""
        session_store = get_session_store(guest_id)

        changed = False
        for key in self.attr_keys:
            value = request.data.get(key)
            if value and session_store[key] != value:
                session_store[key] = value
                changed = True
        session_store.save()

        if changed:
            feature = Feature.objects.get(slug=feature_slug)
            async_to_sync(state.broadcast_feature_state)(feature)

        return Response({**session_store.load(), "id": request.session.session_key})

    def delete(self, request, feature_slug, guest_id):
        """Remove guest and flush profile"""
        feature = get_object_or_404(Feature, slug=feature_slug)

        num_removed: int = feature.guest_queue.remove(guest_id)
        if num_removed:
            error_code = status.HTTP_204_NO_CONTENT
            session_store = get_session_store(guest_id)
            session_store.flush()
            async_to_sync(state.broadcast_feature_state)(feature)

        else:
            error_code = status.HTTP_404_NOT_FOUND

        return Response(status=error_code)
