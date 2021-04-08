from django.db import models
from users.models import User

def get_user_directory(instance, filename):
    return f'uploads/'

class Media(models.Model):
    id = models.AutoField(primary_key=True)
    media = models.FileField(upload_to=get_user_directory, null=True)

class Post(models.Model):
    name = models.CharField(blank=True, max_length=60)
    caption = models.CharField(blank=True, max_length=280)
    status = models.CharField(blank=True, max_length=20)
    owner = models.ForeignKey(User, related_name='Post_owner', null=True, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True)
    multimedia = models.ManyToManyField(Media, related_name='Post', blank=True)

class Comment(models.Model):
    context = models.CharField(blank=True, max_length=280) 
    author = models.ForeignKey(User, related_name='comment_author', null=True, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments', null=True, on_delete=models.CASCADE)

