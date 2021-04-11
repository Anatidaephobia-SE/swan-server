from django.db import models
from users.models import User


def get_teamlogo_directory(instance, filename):
    return f'uploads/teamlogo/{instance.url}/{filename}'


class Team(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(primary_key=True, max_length=100)
    logo = models.ImageField(upload_to=get_teamlogo_directory, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    pending_users = models.ManyToManyField(
        User, related_name='pending_users', blank=True)
    head = models.ForeignKey(
        'users.User', related_name='head', on_delete=models.CASCADE, null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def head_name(self):
        return f'{self.head.first_name} {self.head.last_name}'
