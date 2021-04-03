from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):

    members = serializers.IntegerField(
        source="members.count", read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'url', 'logo',
                  'created_at', 'members', 'head_name']
