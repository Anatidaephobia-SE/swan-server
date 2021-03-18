from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'profile_picture', 'last_login']
