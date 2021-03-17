from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def get_user_directory(instance, filename):
    return f'uploads/userprofile/{instance.username}/{filename}'

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
    verified = models.BooleanField(default=False)
    created_at = models.TimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to=get_user_directory, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]