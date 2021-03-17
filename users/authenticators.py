from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
import jwt
from django.conf import settings
import datetime
class JWTAuthenticator(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        authorized_header = request.headers.get('Authorization')
        if authorized_header is None:
            return None
        try:
            access_token = authorized_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access token expired")
        except IndexError:
            raise  exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        user = User.objects.filter(email=payload['email']).first()
        if(user is None):
            raise exceptions.AuthenticationFailed("user not found")
        return user, access_token

def authenticate(token):
    User = get_user_model()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.filter(email=payload['email']).first()
    except:
        user = AnonymousUser()
    return user

class SimpleAuthenticator(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        authorized_header = request.headers.get('Authorization')
        access_token = ''
        if authorized_header is None:
            return None
        try:
            access_token = authorized_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(email=payload['email']).first()
        except:
            user = AnonymousUser()
        return user, access_token


def generate_access_token(user):
    access_token_payload = {
        'email' : user.email,
        'exp' : datetime.datetime.utcnow() + settings.ACCESS_TOKEN_EXPIRE_TIME,
        'iat' : datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token

def generate_refresh_token(user):
    refresh_token_payload = {
        'email': user.email,
        'exp': datetime.datetime.utcnow() + settings.REFRESH_TOKEN_EXPIRE_TIME,
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return refresh_token