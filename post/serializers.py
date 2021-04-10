from rest_framework import serializers
from . import models
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_picture')

class CommentSerializer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    class Meta:
        model = models.Comment
        fields = ('id','context', 'author','created_at', 'post')
    read_only_fields = ('author')
    
class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ('id','media')

class PostOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email')

class PostSerializer(serializers.ModelSerializer):
    owner = PostOwnerSerializer
    multimedia = PostMediaSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Post
        fields = ('name', 'caption', 'status', 'owner', 'created_at', 'multimedia','team')

