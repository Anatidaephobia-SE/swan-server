from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users import authenticators
from users import email_managment
from .models import User
from .serializers import UserSerializer
from django.core.mail import send_mail

@api_view(['POST'])
@authentication_classes([])
def signup_view(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    confirm_password = request.data.get('confirm_password', None)

    if password != confirm_password:
        return Response({"message": "Passwords does not match"}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    new_user = User(email=email)
    new_user.set_password(password)
    if User.objects.filter(email=email).exists():
        return Response({"message": "This user already exists"}, status=status.HTTP_400_BAD_REQUEST)

    token = authenticators.generate_access_token(new_user)
    email_managment.send_mail(token, email)
    # send_mail("Yo!", token, "admin@swan-app.ir", [email], fail_silently=False)
    new_user.save()
    return Response({"message": "Successful. Mail sent to user."}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile_picture = request.data.get('profile_picture', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    if first_name is None:
        return Response({"error": "First name not submitted."}, status=status.HTTP_400_BAD_REQUEST)
    if last_name is None:
        return Response({"error": "Last name not submitted."}, status=status.HTTP_400_BAD_REQUEST)

    if profile_picture or profile_picture == "":
        if(profile_picture == ""):
            profile_picture = None
        user.profile_picture = profile_picture

    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return Response({"user": UserSerializer(user).data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request, user_email=None):
    print(user_email)
    if user_email is None:
        user = request.user
    else:
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
def login_view(request):
    email = request.data.get('email', None)
    password = request.data.get("password", None)
    if email is None:
        return Response({"message": "First name not submitted."}, status=status.HTTP_400_BAD_REQUEST)
    User = get_user_model()

    user = authenticate(email=email, password=password)
    if user is None:
        return Response({"message": "Wrong user name password"}, status=status.HTTP_401_UNAUTHORIZED)

    token = authenticators.generate_access_token(user)
    user_serializer = UserSerializer(user)
    if user.verified:
        return Response({"token": token, "user": user_serializer.data}, status=status.HTTP_200_OK)
    else:
        email_managment.send_mail(token, email)
        return Response({"message": "User not verified. Mail sent to email."}, status=status.HTTP_403_FORBIDDEN)

@api_view(["POST"])
def send_email(request):
    email = request.data.get("email", "hadisheikhi77@gmail.com")
    token = "A beuteaful token!"
    send_mail("Yo!", token, "admin@swan-app.ir", [email], fail_silently=False)