from rest_framework import serializers
from .models import SocialMedia


class SocialMediaSatisfier(serializers.ModelSerializer):
    has_twitter = serializers.SerializerMethodField()
    def get_has_twitter(self, intsance):
        return intsance.twitter_user_id is not None
    class Meta:
        model = SocialMedia
        fields = ['has_twitter']
