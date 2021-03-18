from rest_framework import serializers
from .models import team

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = team
        fields = ['name', 'url', 'logo', 'created_at']