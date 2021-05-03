from rest_framework import serializers
from users.models import User
from .models import MediaStorage
from swan.settings import MINIO_ENDPOINT

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_picture')

class FileSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    
    def edit_url(self,obj):
        return obj.media.replace(MINIO_ENDPOINT, os.getenv("BASE_URL_FOR_MINIO"))
    class Meta:
        model = MediaStorage
        fields = ('id','media','team','owner')
    read_only_fields = ('owner','team')    


