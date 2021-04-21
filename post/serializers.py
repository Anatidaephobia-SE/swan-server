from rest_framework import serializers
from . import models
from users.models import User

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

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    multimedia = PostMediaSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Post
        fields = ('id','name', 'caption', 'status', 'owner', 'created_at', 'multimedia','team')
    read_only_fields = ('owner','id')

class UpdatePostSerializer(serializers.ModelSerializer):
    multimedia = PostMediaSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Post
        fields = ('id','name', 'caption', 'status', 'multimedia','team')
    read_only_fields = ('id')