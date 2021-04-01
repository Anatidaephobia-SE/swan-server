from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class SocialMedia(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    twitter_oauth_token = models.TextField(null=True, max_length=200)
    twitter_oauth_token_secret = models.TextField(null=True, max_length=200)
    twitter_user_id = models.TextField(null=True, max_length=200)
    twitter_name = models.TextField(null=True, max_length=200)