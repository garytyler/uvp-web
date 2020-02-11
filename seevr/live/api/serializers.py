from rest_framework import serializers

from seevr.live.models import Feature, Guest
from seevr.live.utils import get_sessions


class FeatureSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    turn_duration = serializers.DurationField(read_only=True)
    guest_queue = serializers.SerializerMethodField()

    class Meta:
        model = Feature
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_guest_queue(self, instance):
        return get_sessions(list(instance.guest_queue))


class GuestSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.SerializerMethodField()
    name = serializers.CharField()
    session_key = serializers.SerializerMethodField(read_only=True)
    feature = serializers.SlugRelatedField(
        slug_field="slug", queryset=Feature.objects.all()
    )

    class Meta:
        model = Guest
        exclude: list = []

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_session_key(self, instance):
        return instance.session_key
