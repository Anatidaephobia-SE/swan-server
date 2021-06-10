from django.db import models
from team.models import Team

class Email(models.Model):

    template_name = models.CharField(null = True, max_length=60)
    body_text = models.CharField(blank = True, max_length=700)
    subject= models.CharField(blank = True, max_length=280)
    reciviers = models.TextField(null=False, max_length=1000)
    sender = models.ForeignKey(Team, related_name = 'team_email', null = True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    schedule_time = models.DateTimeField(blank=True, null=True)

class EmailAPI(models.Model):
    url = models.TextField(null=False, max_length=200)