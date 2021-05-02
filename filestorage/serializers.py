from rest_framework import serializers
from users.models import User
from .models import MediaStorage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_picture')

class FileSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    class Meta:
        model = MediaStorage
        fields = ('id','title','media','team','owner')
    read_only_fields = ('owner','team')    


