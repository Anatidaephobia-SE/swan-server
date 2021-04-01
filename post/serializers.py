from rest_framework import serializers
from . import models
from users.models import User

class PostOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ('id','media')

class PostSerializer(serializers.ModelSerializer):
    owner = PostOwnerSerializer
    gallery = PostMediaSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = models.Post
        fields = ('name', 'caption', 'status', 'owner', 'created_at', 'multimedia')
        read_only_fields = ('games', )


