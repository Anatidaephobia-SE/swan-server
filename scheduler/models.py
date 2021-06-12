from django.db import models
from enum import IntEnum
from post.models import Post
from notification.models import Email
# Create your models here.

class TaskType(IntEnum):
    Email = 1
    Twitter = 2

class TaskState(IntEnum):
    Active = 1
    Queued = 2
    Done = 3

class Tasks(models.Model):
    task_type = models.IntegerField(null=False)
    body = models.TextField(max_length=10000)
    create_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=False)
    state = models.IntegerField(null=False)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    mail = models.ForeignKey(Email, null=True, on_delete=models.CASCADE)