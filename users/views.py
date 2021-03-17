from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework import status
import users.authenticators as Authenticator
import users.email_managment as EmailManager
# Create your views here.


@api_view(['POST'])
def signup_view(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    User = get_user_model()
    new_user = User(email=email)
    new_user.set_password(password)
    if(User.objects.filter(email=email).exists()):
        return JsonResponse({"message" : "Same user exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    token =  Authenticator.generate_access_token(new_user)
    EmailManager.send_mail(token, email)
    new_user.save()
    return JsonResponse({"message" : "Successful. Mail sent to user"}, status=status.HTTP_200_OK)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    pass