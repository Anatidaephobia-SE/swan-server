from django.shortcuts import render
from .models import Team
from users.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.http.response import JsonResponse
from request_checker.functions import *
from .serializers import TeamSerializer
from users.serializers import UserSerializer
from django.db.models import Q

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):

    user = request.user

    req_check = have_parameters(request, 'name', 'url')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    name = request.data.get('name')
    url = request.data.get('url')
    logo = request.data.get('logo', None)

    if Team.objects.filter(url = url).exists():
        return JsonResponse({'error' : 'Team with same url exists'})

    new_team = Team(name = name, url = url, logo = logo, head = user)
    new_team.save()

    return JsonResponse({"message" : "Team created successfuly"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_user(request):
    head = request.user

    req_check = have_parameters(request, 'team_url', 'username')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    team_url = request.data.get('team_url')
    username = request.data.get('username')

    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with this url does not exist'}, status = status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(username = username).first()
    if user is None:
        return JsonResponse({'error' : 'User with this username does not exist'}, status = status.HTTP_404_NOT_FOUND)

    if Team.objects.filter(Q(pk = team_url, pending_users__pk = user.id) | Q(pk = team_url, members__pk = user.id)).exists():
        return JsonResponse({'error' : 'User already invited or joined to team'}, status = status.HTTP_400_BAD_REQUEST)

    if team.head != head:
        return JsonResponse({'error' : 'This user is not head of team'}, status = status.HTTP_403_FORBIDDEN)
    
    team.pending_users.add(user)

    return JsonResponse({'message' : 'User invited successfuly'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invite(request):
    user = request.user

    req_check = have_parameters(request, 'team_url')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    team_url = request.data.get('team_url')

    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with url does not exist'}, status = status.HTTP_404_NOT_FOUND)

    if not Team.objects.filter(pk = team_url, pending_users__pk = user.id).exists():
        return JsonResponse({'error' : 'User is not invited to team'}, status = status.HTTP_403_FORBIDDEN)
    
    team.pending_users.remove(user)
    team.members.add(user)

    return JsonResponse({'message' : 'User joined team successfuly'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_invite(request):
    user = request.user

    req_check = have_parameters(request, 'team_url')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    team_url = request.data.get('team_url')

    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with url does not exist'}, status = status.HTTP_404_NOT_FOUND)

    if not Team.objects.filter(pk = team_url, pending_users__pk = user.id).exists():
        return JsonResponse({'error' : 'User is not invited to team'}, status = status.HTTP_403_FORBIDDEN)
    
    team.pending_users.remove(user)

    return JsonResponse({'message' : 'User rejected invite successfuly'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_user(request):
    head = request.user

    req_check = have_parameters(request, 'team_url', 'username')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    team_url = request.data.get('team_url')
    username = request.data.get('username')

    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with this url does not exist'}, status = status.HTTP_404_NOT_FOUND)
    
    user = User.objects.filter(username = username).first()
    if user is None:
        return JsonResponse({'error' : 'User with this username does not exists'}, status = status.HTTP_404_NOT_FOUND)
    
    if team.head != head:
        return JsonResponse({'error' : 'This user is not head of team'}, status = status.HTTP_403_FORBIDDEN)

    team.members.remove(user)

    return JsonResponse({'message' : 'User removed successfuly'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_team(request):
    user = request.user

    req_check = have_parameters(request, 'team_url')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)
    
    team_url = request.data.get('team_url')
    
    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with this url does not exist'}, status = status.HTTP_404_NOT_FOUND)

    team.members.remove(user)

    return JsonResponse({'message' : 'User left the team'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invites(request):
    user = request.user

    teams = Team.objects.filter(pending_users__pk = user.id)
    
    return JsonResponse({'teams' : TeamSerializer(teams, many = True).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_team_info(request):

    req_check = have_queryparams(request, 'team_url')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    team_url = request.query_params.get('team_url')

    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with this url does not exist'}, status = status.HTTP_404_NOT_FOUND)
    
    return JsonResponse({'team' : TeamSerializer(team).data})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_members(request):

    req_check = have_queryparams(request, 'team_url')
    if not req_check.have_all: return JsonResponse({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)
    
    team_url = request.query_params.get('team_url')

    team = Team.objects.filter(url = team_url).first()
    if team is None:
        return JsonResponse({'error' : 'Team with this url does not exist'}, status = status.HTTP_404_NOT_FOUND)
    
    members = team.members.all()
    return JsonResponse({'members' : UserSerializer(members, many = True).data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_teams(request):
    user = request.user

    teams = Team.objects.filter(members__pk = user.id)

    return JsonResponse({'teams' : TeamSerializer(teams, many = True).data})
    