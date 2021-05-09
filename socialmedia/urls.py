

from django.urls import path
from .views import twitter_request_authorize, twitter_access, get_user, get_trends, get_tweet_info

urlpatterns = [
    path('twitter/authorize/request', twitter_request_authorize, name="requestAuthorizeTwitter"),
    path('twitter/authorize/access', twitter_access, name="accessTwitter"),
    path('twitter/accounts', get_user, name="accountsTwitter"),
    path('twitter/get_trends', get_trends, name="trendsTwitter"),
    path('twitter/tweet/',get_tweet_info, name="TweetDetail")
]
