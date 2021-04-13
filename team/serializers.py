from rest_framework import serializers
from .models import Team
from users.models import User


class TeamSerializer(serializers.ModelSerializer):

    members = serializers.IntegerField(
        source="members.count", read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'url', 'logo',
                  'created_at', 'members', 'head_name']
    read_only_fields = ('id')

class MemberSerializer(serializers.ModelSerializer):

    is_head = serializers.SerializerMethodField()

    def get_is_head(self, instance):
        return self.context.get('is_head')
        
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'profile_picture', 'last_login', 'is_head']
