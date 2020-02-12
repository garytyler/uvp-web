from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from seevr.live.api.serializers import FeatureSerializer
from seevr.live.models import Feature


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    lookup_field = "slug"


class GuestAPIView(APIView):
    def get(self, request, format=None):
        guest_name = request.session.get("name")
        if not guest_name:
            raise Http404
        return Response({"name": guest_name})

    def post(self, request, format=None):
        guest_name = request.data.get("name")
        if not guest_name:
            return Response("Name is required.", status=status.HTTP_400_BAD_REQUEST,)
        else:
            request.session["name"] = guest_name
            request.session.save()
            return Response({"name": request.session["name"]})
