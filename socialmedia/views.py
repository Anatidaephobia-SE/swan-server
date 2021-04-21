from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from .twitter import Authorize_Address, Get_Access_Token, Queue_Tweet, Tweet, Get_Twitter_User
from rest_framework.response import Response
from rest_framework import status, generics
from .models import SocialMedia
from team.models import Team
from post.models import Post
from request_checker.functions import *
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def twitter_request_authorize(request):
    req_check = have_parameters(request, 'team_id')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
    team_id = request.data.get("team_id")
    modify = request.data.get("modify", 0)
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response(data={"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if(user.email != team.head.email):
        return Response(data={"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    message, status_code = Authorize_Address(team_id, modify)
    if(status_code != 200):
        return Response(data={"error": message}, status=status_code)
    return Response(data={"address": message}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def twitter_access(request):
    req_check = have_parameters(
        request, 'oauth_token', 'oauth_verifier', 'team_id')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    oauth_token = request.data.get("oauth_token")
    oauth_verifier = request.data.get("oauth_verifier")
    team_id = request.data.get("team_id")
    try:
        team = Team.objects.get(id=team_id)
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

@api_view(["GET"])
def get_user(request):
    user = request.user
    req_check = have_queryparams(request, 'team_id')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
    team_id = request.query_params.get("team_id")

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response(data={"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        social_media = SocialMedia.objects.get(team=team)
    except SocialMedia.DoesNotExist:
        return Response(data={"error": "Social media accounts for this team not found"}, status=status.HTTP_404_NOT_FOUND)
    if(social_media.twitter_user_id is None):
        return Response(data={"error": "Team don't have twitter."}, status=status.HTTP_403_FORBIDDEN)
    response = Get_Twitter_User(social_media.twitter_user_id)
    if(response.status_code != 200):
        return Response(data=response.json(), status=response.status_code)
    json = response.json()[0]
    data = {
        "name": json["name"], 
        "profile_image": json["profile_image_url"], 
        "screen_name" : json['screen_name'],
        "default_profile_image" : json["default_profile_image"]
    }
    return Response(data=data, status=response.status_code)