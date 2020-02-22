from rest_framework import serializers

from seevr.live.models import Feature, Guest
from seevr.live.utils import get_session


class FeatureSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    turn_duration = serializers.DurationField(read_only=True)
    guests = serializers.SerializerMethodField()
    presenter_channel = serializers.CharField()

    class Meta:
        model = Feature
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_guests(self, instance):
        result = []
        for session_key in instance.guest_queue:
            session_store = get_session(session_key)
            session_store["id"] = session_key
            result.append(session_store)
        return result

    def get_presenter_channel(self, instance):
        result = []
        for session_key in instance.guest_queue:
            session_store = get_session(session_key)
            session_store["id"] = session_key
            result.append(session_store)
        return result


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
