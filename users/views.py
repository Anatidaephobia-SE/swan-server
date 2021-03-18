from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework import status
import users.authenticators as Authenticator
import users.email_managment as EmailManager
from .serializers import UserSerializer
from django.contrib.auth import authenticate
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
    return JsonResponse({"message" : "Successful. Mail sent to user."}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile_picture = request.data.get('profile_picture', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    if(first_name is None):
        return JsonResponse({"error" : "First name not submitted."}, status=status.HTTP_400_BAD_REQUEST)
    if(first_name is None):
        return JsonResponse({"error" : "Last name not submitted."}, status=status.HTTP_400_BAD_REQUEST)
    user.profile_picture = profile_picture
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return JsonResponse({"user" : UserSerializer(user).data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email', None)
    password = request.data.get("password", None)
    if(email is None):
        return JsonResponse({"message" : "First name not submitted."}, status=status.HTTP_400_BAD_REQUEST)
    User = get_user_model()
    try:
        user = authenticate(email=email, password=password)
        if user is None:
            return JsonResponse({"message" : "Wrong user name password"}, status=status.HTTP_401_UNAUTHORIZED)
        token = Authenticator.generate_access_token(user)
        if(user.verified):
            return JsonResponse({"access_token" : token}, status=status.HTTP_200_OK)
        else:
            EmailManager.send_mail(token, email)
            return JsonResponse({"message" : "User not verified. Mail sent to email."}, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        return JsonResponse({"message" : "Wrong user name password"}, status=status.HTTP_401_UNAUTHORIZED)
    