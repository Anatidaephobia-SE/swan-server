

from django.urls import path
from .views import twitter_request_authorize, twitter_access, get_user, get_trends

urlpatterns = [
    path('twitter/authorize/request', twitter_request_authorize),
    path('twitter/authorize/access', twitter_access),
    path('twitter/accounts', get_user),
    path('twitter/get_trends', get_trends)
]
