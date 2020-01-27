from rest_framework import serializers

from seevr.live.models import Feature, Guest


class GuestSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    session_key = serializers.SerializerMethodField(read_only=True)
    feature = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Guest
        exclude: list = []

    def get_feature(self, instance):
        return instance.feature.slug

    def get_session_key(self, instance):
        request = self.context.get("request")
        print(request.session.session_key)
        return request.session.session_key


class FeatureSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    turn_duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Feature
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")
