from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from seevr.live.api.serializers import FeatureSerializer, GuestSerializer
from seevr.live.models import Feature, Guest

# from rest_framework.views import APIView
# from rest_framework.response import Response


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    lookup_field = "slug"
    serializer_class = FeatureSerializer
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(title=self.request.user)

    def initialize_request(self, request, *args, **kwargs):
        """
        Set the `.action` attribute on the view, depending on the request method.
        """

        request = super().initialize_request(request, *args, **kwargs)

        method = request.method.lower()
        if method == "options":
            # This is a special case as we always provide handling for the
            # options method in the base `View` class.
            # Unlike the other explicitly defined actions, 'metadata' is implicit.
            self.action = "metadata"
        else:
            self.action = self.action_map.get(method)
        return request


class GuestCreateAPIView(generics.CreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        self.request.session.save()
        request_session_key = self.request.session.session_key
        kwarg_slug = self.kwargs.get("slug")
        feature = get_object_or_404(Feature, slug=kwarg_slug)

        if request_session_key in feature.guest_queue:
            raise ValidationError("You are already in the queue!")

        serializer.save(session_key=request_session_key, feature=feature)


class GuestListAPIView(generics.ListAPIView):
    serializer_class = GuestSerializer
    # permission_class = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Guest.objects.filter(feature__slug=kwarg_slug)


# class GuestViewSet(viewsets.ModelViewSet):
#     queryset = Guest.objects.all()
#     lookup_field = "session_key"
#     serializer_class = GuestSerializer

# def perform_create(self, serializer):
#     session_key = self.request.session.session_key
#     kwarg_slug = self.kwargs.get("slug")
#     serializer
#     serializer.save(author=self.request.user)


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ["url", "username", "email", "groups"]
