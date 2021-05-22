from rest_framework import serializers
from . import models
from users.models import User
from filestorage.models import MediaStorage
from swan.settings import MINIO_ENDPOINT
import os
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'profile_picture')
    read_only_fields = ('id')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    class Meta:
        model = models.Comment
        fields = ('id','context', 'author','created_at', 'post')
    read_only_fields = ('author','id')
    
class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ('id','media')
    read_only_fields = ('id')

class StorageSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    def get_media(self, instance):
        return str(instance.media.url).replace(MINIO_ENDPOINT, os.getenv("BASE_URL_FOR_MINIO")).replace("http", "https")
    class Meta:
        model = MediaStorage
        fields = ('id','media')
    read_only_fields = ('id', 'media')

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    multimedia = StorageSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Post
        fields = ('id','name', 'caption', 'status', 'owner', 'created_at', 'multimedia','team','tag','schedule_time')
    read_only_fields = ('owner','id')

class UpdatePostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    multimedia = StorageSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Post
        fields = ('id','name', 'caption', 'status', 'multimedia','team','tag','schedule_time', 'owner')
    read_only_fields = ('id')