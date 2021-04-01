from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from .twitter import Authorize_Address, Get_Access_Token
from rest_framework.response import Response
from rest_framework import status
from .models import SocialMedia
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def twitter_request_authorize(request):
    message, status_code = Authorize_Address()
    if(status_code != 200):
        return Response(data={"error": message}, status=status_code)
    return Response(data={"address": message}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def twitter_access(request):
    user = request.user
    oauth_token = request.data.get("oauth_token", None)
    oauth_verifier = request.data.get("oauth_verifier", None)
    if(oauth_token is None or oauth_verifier is None):
        return Response(data={"error": "Oauth token or verifier not set."}, status=status.HTTP_400_BAD_REQUEST)
    data, status_code = Get_Access_Token(oauth_token, oauth_verifier)
    if(status_code != 200):
        return Response(data={"error": data}, status=status_code)
    twitter_data = {}
    for entry in data.split('&'):
        key, value = tuple(entry.split('='))
        twitter_data[key] = value
    try:
        social_media = SocialMedia.objects.get(user=user)
    except:
        social_media = SocialMedia.objects.create(user=user)
    social_media.twitter_oauth_token = twitter_data['oauth_token']
    social_media.twitter_oauth_token_secret = twitter_data['oauth_token_secret']
    social_media.twitter_user_id = twitter_data['user_id']
    social_media.twitter_name = twitter_data['screen_name']
    social_media.save()
    return Response(data={"message": "Successful."}, status=status.HTTP_200_OK)
