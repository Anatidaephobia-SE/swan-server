from django.urls import path
from .views import *

urlpatterns = [
    path('create_team', create_team, name="createTeam"),
    path('invite_user', invite_user, name="inviteUser"),
    path('accept_invite', accept_invite, name="acceptInvite"),
    path('reject_invite/<team_id>/', reject_invite, name="rejectInvite"),
    path('remove_user/<team_id>/', remove_user, name="removeUser"),
    path('leave_team/<team_id>/', leave_team, name="leaveTeam"),
    path('get_invites', get_invites, name="getInvites"),
    path('get_team_info', get_team_info, name="getTeamInfo"),
    path('get_members', get_members, name="getMembers"),
    path('get_user_teams', get_user_teams, name="getUserTeams"),
    path('update_team_info', update_team_info, name="updateTeamInfo"),
]
