from django.db import models
from team.models import Team


# Create your models here.
class SocialMedia(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    twitter_oauth_token = models.TextField(null=True, max_length=200)
    twitter_oauth_token_secret = models.TextField(null=True, max_length=200)
    twitter_user_id = models.TextField(null=True, max_length=200)
    twitter_name = models.TextField(null=True, max_length=200)