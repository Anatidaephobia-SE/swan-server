from django.urls import path
from .views import *

urlpatterns = [
    path('create_team', create_team),
    path('invite_user', invite_user),
    path('accept_invite', accept_invite),
    path('reject_invite/<team_id>/', reject_invite),
    path('remove_user/<team_id>/', remove_user),
    path('leave_team/<team_id>/', leave_team),
    path('get_invites', get_invites),
    path('get_team_info', get_team_info),
    path('get_members', get_members),
    path('get_user_teams', get_user_teams),
    path('update_team_info', update_team_info),
]
