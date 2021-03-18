from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create_team', create_team),
    url(r'^invite_user', invite_user),
]