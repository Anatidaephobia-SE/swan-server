

from django.urls import path
from .views import twitter_request_authorize, twitter_access

urlpatterns = [
    path('twitter/authorize/request', twitter_request_authorize),
    path('twitter/authorize/access', twitter_access)
]