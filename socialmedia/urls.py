

from django.urls import path
from .views import twitter_request_authorize, twitter_access, tweet, get_user

urlpatterns = [
    path('twitter/authorize/request', twitter_request_authorize),
    path('twitter/authorize/access', twitter_access),
    path('twitter/accounts/tweet', tweet),
    path('twitter/accounts', get_user)
]
