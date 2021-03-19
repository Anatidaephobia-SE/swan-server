from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create_team', create_team),
    url(r'^invite_user', invite_user),
    url(r'^accept_invite', accept_invite),
    url(r'^reject_invite', reject_invite),
    url(r'^remove_user', remove_user),
    url(r'^leave_team', leave_team),
    url(r'^get_invites', get_invites),
    url(r'^get_team_info', get_team_info),
    url(r'^get_members', get_members),
    url(r'^get_user_teams', get_user_teams),
]