from django.shortcuts import render
from .models import Team
from users.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from request_checker.functions import *
from .serializers import TeamSerializer, MemberSerializer
from users.serializers import UserSerializer
from django.db.models import Q
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):

    user = request.user

    req_check = have_parameters(request, 'name', 'url')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    name = request.data.get('name')
    url = request.data.get('url')
    logo = request.data.get('logo', None)

    if Team.objects.filter(url=url).exists():
        return Response({'error': 'Team with same url exists'})

    new_team = Team(name=name, url=url, logo=logo, head=user)
    new_team.save()
    new_team.members.add(user)

    return Response({'team': TeamSerializer(new_team).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_user(request):
    head = request.user

    req_check = have_parameters(request, 'team_id', 'username')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    team_id = request.data.get('team_id')
    username = request.data.get('username')

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(username=username).first()
    if user is None:
        return Response({'error': 'User with this username does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if Team.objects.filter(Q(id=team_id, pending_users__id=user.id) | Q(id=team_id, members__id=user.id)).exists():
        return Response({'error': 'User already invited or joined to team'}, status=status.HTTP_400_BAD_REQUEST)

    if team.head != head or not Team.objects.filter(members__id = head.id).exists():
        return Response({'error': 'This user is not head of team'}, status=status.HTTP_403_FORBIDDEN)

    team.pending_users.add(user)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invite(request):
    user = request.user

    req_check = have_parameters(request, 'team_id')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    team_id = request.data.get('team_id')

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not Team.objects.filter(id=team_id, pending_users__pk=user.id).exists():
        return Response({'error': 'User is not invited to team'}, status=status.HTTP_403_FORBIDDEN)

    team.pending_users.remove(user)
    team.members.add(user)

    return Response({'message': 'User joined team successfuly'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_invite(request, team_id):
    user = request.user

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not Team.objects.filter(id=team_id, pending_users__pk=user.id).exists():
        return Response({'error': 'User is not invited to team'}, status=status.HTTP_403_FORBIDDEN)

    team.pending_users.remove(user)

    return Response({'message': 'User rejected invite successfuly'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_user(request, team_id):
    head = request.user

    req_check = have_queryparams(request, 'username')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    username = request.query_params.get('username')

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(username=username).first()
    if user is None:
        return Response({'error': 'User with this username does not exists'}, status=status.HTTP_404_NOT_FOUND)

    if team.head != head:
        return Response({'error': 'This user is not head of team'}, status=status.HTTP_403_FORBIDDEN)

    if team.head == user:
        return Response({'error' : 'Head of team can not be removed'}, status = status.HTTP_403_FORBIDDEN)

    team.members.remove(user)

    return Response({'message': 'User removed successfuly'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_team(request, team_id):
    user = request.user

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if team.head == user:
        return Response({'error' : 'Head of team can not leave the team'}, status = status.HTTP_403_FORBIDDEN)

    team.members.remove(user)

    return Response({'message': 'User left the team'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invites(request):
    user = request.user

    teams = Team.objects.filter(pending_users__pk=user.id)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_info(request):
    user = request.user

    req_check = have_queryparams(request, 'team_id')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    team_id = request.query_params.get('team_id')

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not Team.objects.filter(members__id = user.id).exists():
        return Response({'error' : 'This user is not member of team'}, status = status.HTTP_403_FORBIDDEN)

    return Response({'team': TeamSerializer(team).data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_members(request):
    user = request.user

    req_check = have_queryparams(request, 'team_id')
    if not req_check.have_all:
        return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)

    team_id = request.query_params.get('team_id')

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error': 'Team with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not Team.objects.filter(members__id = user.id).exists():
        return Response({'error' : 'This user is not member of team'}, status = status.HTTP_403_FORBIDDEN)

    members = team.members.all()
    serialized = []
    for member in members:
        serialized.append(MemberSerializer(member, context = {'is_head' : team.head.id == member.id}).data)
    return Response({'members': serialized})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_teams(request):
    user = request.user

    teams = Team.objects.filter(members__pk=user.id)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_team_info(request):
    head = request.user

    req_check = have_parameters(request, 'team_id')
    if not req_check.have_all: return Response({'error' : req_check.error_message}, status = status.HTTP_400_BAD_REQUEST)

    team_id = request.data.get('team_id')

    team = Team.objects.filter(id=team_id).first()
    if team is None:
        return Response({'error' : 'Team with this id does not exist'}, status = status.HTTP_404_NOT_FOUND)
    
    if team.head != head:
        return Response({'error' : 'This user is not head of team'}, status = status.HTTP_403_FORBIDDEN)
    
    new_logo = request.data.get('logo', None)
    new_name = request.data.get('name', None)
    new_url = request.data.get('url', None)

    if new_logo != None:
        team.logo = new_logo
        team.save(update_fields = ['logo'])
    if new_name != None:
        team.name = new_name
        team.save(update_fields = ['name'])
    if new_url != None:
        if Team.objects.filter(url = new_url).exists():
            return Response({'error' : 'Team with this url already exists'})
    
        team.url = new_url
        team.save(update_fields = ['url'])
    
    return Response({'message' : 'All fields updated'})