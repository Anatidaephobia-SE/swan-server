from rest_framework import serializers
from . import models
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'profile_picture')
    read_only_fields = ('id')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ('id','title', 'description','status', 'assignee', 'created_at', 'team','tag')
    read_only_fields = ('id')

class CardAssigneeSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(required=False)
    class Meta:
        model = models.Card
        fields = ('id','title', 'description','status', 'assignee', 'created_at', 'team','tag')
    read_only_fields = ('assignee','id')

    
