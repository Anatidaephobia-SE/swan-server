from django.db import models
from django.contrib.auth.models import AbstractUser


def get_user_directory(instance, filename):
    return f'userprofile/{instance.id}/{filename}'


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, db_index=True)
    username = models.CharField(unique=False, max_length=52)
    verified = models.BooleanField(default=False)
    created_at = models.TimeField(auto_now_add=True)
    profile_picture = models.ImageField(
        upload_to=get_user_directory, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email
