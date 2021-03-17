from django.shortcuts import render
from .models import team
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_team(request):

#     user = request.user

#     name = request.data.get('name', None)
#     url = request.data.get('url', None)
#     logo = request.data.get('logo', None)

#     if (name is None) or (url is None):
#         return JsonResponse({"error" : "name and url parameters required"})
#     if team.objects.filter(url = url).exists():
#         return JsonResponse({'error' : 'Team with same url exists'})

#     new_team = team(name = name, url = url, logo = logo, head = user)
#     new_team.save()

#     return JsonResponse({"message" : "Team created successfuly"})

# temparary view for create team(without login)
@api_view(['POST'])
def create_team(request):

    user = request.user

    name = request.data.get('name', None)
    url = request.data.get('url', None)
    logo = request.data.get('logo', None)

    if (name is None) or (url is None):
        return JsonResponse({'error' : 'Name and url parameters required'})
    if team.objects.filter(url = url).exists():
        return JsonResponse({'error' : 'Team with same url exists'})
    
    new_team = team(name = name, url = url, logo = logo)
    new_team.save()

    return JsonResponse({'message' : 'Team created successfuly'})
