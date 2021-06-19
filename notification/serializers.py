from rest_framework import serializers
from . import models
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'profile_picture')
    read_only_fields = ('id')

class TemplateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    class Meta:
        model = models.Template
        fields = ('id','name', 'body_text', 'subject', 'reciviers','sender','template_team','created_at','schedule_time','status','owner')
    read_only_fields = ('id',)

class UpdateTemplateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    class Meta:
        model = models.Template
        fields = ('id','name', 'body_text', 'subject', 'reciviers','sender','template_team','schedule_time','status','owner')
    read_only_fields = ('id',)

# class PostSerializer(serializers.ModelSerializer):
#     owner = UserSerializer(required=False)
#     multimedia = StorageSerializer(many=True, read_only=True, required=False)
#     class Meta:
#         model = models.Post
#         fields = ('id','name', 'caption', 'status', 'owner', 'created_at', 'multimedia','team','tag','schedule_time')
#     read_only_fields = ('owner','id')

# class UpdatePostSerializer(serializers.ModelSerializer):
#     owner = UserSerializer(required=False)
#     multimedia = StorageSerializer(many=True, read_only=True, required=False)
#     class Meta:
#         model = models.Post
#         fields = ('id','name', 'caption', 'status', 'multimedia','team','tag','schedule_time', 'owner')
#     read_only_fields = ('id')