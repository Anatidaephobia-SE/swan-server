from rest_framework import serializers
from users.models import User
from .models import MediaStorage
from swan.settings import MINIO_ENDPOINT
import os

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_picture')

class FileSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    media = serializers.SerializerMethodField()
    def get_media(self, instance):
        return str(instance.media.url).replace(MINIO_ENDPOINT, os.getenv("BASE_URL_FOR_MINIO")).replace("http", "https")
    class Meta:
        model = MediaStorage
        fields = ('id','media','team','owner')
    read_only_fields = ('owner','team')    


