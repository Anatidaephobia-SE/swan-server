from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from .twitter import Authorize_Address, Get_Access_Token, Queue_Tweet, Tweet
from rest_framework.response import Response
from rest_framework import status
from .models import SocialMedia
from team.models import Team
from request_checker.functions import *
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def twitter_request_authorize(request):
    req_check = have_parameters(request, 'team_url')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
    team_url = request.data.get("team_url")
    try:
        team = Team.objects.get(url=team_url)
    except Team.DoesNotExist:
        return Response(data={"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if(user.email != team.head.email):
        return Response(data={"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    message, status_code = Authorize_Address(team_url)
    if(status_code != 200):
        return Response(data={"error": message}, status=status_code)
    return Response(data={"address": message}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def twitter_access(request):
    req_check = have_parameters(
        request, 'oauth_token', 'oauth_verifier', 'team_url')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    oauth_token = request.data.get("oauth_token")
    oauth_verifier = request.data.get("oauth_verifier")
    team_url = request.data.get("team_url")
    try:
        team = Team.objects.get(url=team_url)
    except Team.DoesNotExist:
        return Response(data={"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    data, status_code = Get_Access_Token(oauth_token, oauth_verifier)
    if(status_code != 200):
        return Response(data={"error": data}, status=status_code)
    twitter_data = {}
    for entry in data.split('&'):
        key, value = tuple(entry.split('='))
        twitter_data[key] = value
    try:
        social_media = SocialMedia.objects.get(team=team)
    except:
        social_media = SocialMedia.objects.create(team=team)
    social_media.twitter_oauth_token = twitter_data['oauth_token']
    social_media.twitter_oauth_token_secret = twitter_data['oauth_token_secret']
    social_media.twitter_user_id = twitter_data['user_id']
    social_media.twitter_name = twitter_data['screen_name']
    social_media.save()
    return Response(data={"message": "Successful."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet(request):
    user = request.user
    req_check = have_parameters(request, 'post_id', 'team_url')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
    team_url = request.data.get("team_url")
    post_id = request.data.get("post_id")
    text = "Hola!"
    try:
        team = Team.objects.get(url=team_url)
        social_media = SocialMedia.objects.get(team=team)
    except Team.DoesNotExist:
        return Response(data={"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        social_media = SocialMedia.objects.get(team=team)
    except SocialMedia.DoesNotExist:
        return Response(data={"error": "Social media accounts not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        #TODO find post
        pass
    except:
        pass
    Tweet(text, social_media) #TODO Queue_Tweet(post, ...)
    return Response(data={"message": "Successful."}, status=status.HTTP_200_OK)