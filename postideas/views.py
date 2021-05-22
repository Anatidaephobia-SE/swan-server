from django.db.models.fields import NullBooleanField
from django.http.response import JsonResponse
from postideas.models import Card
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as Card_Serializer
from users.models import User
from team.models import Team
from request_checker.functions import *
import json

class CreateCardView(generics.CreateAPIView):
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = Card_Serializer.CardSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        card_workspace=Team.objects.get(pk=data['team'])
        card_title=data['title']
        card_description=data['description']
        card_status=data['status']
        card = Card(team=card_workspace,title=card_title,description=card_description,status=card_status)
        if 'tag' in data:
            card.tag=data['tag']
            card.save()
        if 'assignee' in data:
            card_assignee = User.objects.get(pk=data['assignee'])
            card.assignee=card_assignee
            card.save()
        card.save()
        return Response(Card_Serializer.CardAssigneeSerializer(card).data, status=status.HTTP_201_CREATED)
 
class AllCardstView(generics.ListAPIView):
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = Card_Serializer.CardAssigneeSerializer

    def get(self, request,pk=None):
        team_pk = pk
        cradlistDone = Card.objects.filter(team=team_pk).filter(status="done")
        cradlistInProgress = Card.objects.filter(team=team_pk).filter(status="inProgress")
        cradlistToDo = Card.objects.filter(team=team_pk).filter(status="todo")
        workspace_cards={}
        workspace_cards['todo'] = Card_Serializer.CardAssigneeSerializer(cradlistToDo, many=True).data
        workspace_cards['inProgress'] = Card_Serializer.CardAssigneeSerializer(cradlistInProgress, many=True).data
        workspace_cards['done'] = Card_Serializer.CardAssigneeSerializer(cradlistDone, many=True).data
        return Response(workspace_cards, status=status.HTTP_200_OK)

class DeleteCardView(generics.UpdateAPIView):

    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = Card_Serializer.CardAssigneeSerializer

    def delete(self, request,pk=None):
        card_pk = pk
        user = request.user
        card_info = Card.objects.get(pk=card_pk)
        card_info.delete()
        return Response("Card deleted.", status=status.HTTP_200_OK)


class MoveCardView(generics.UpdateAPIView):

    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = Card_Serializer.CardAssigneeSerializer

    def put(self, request,pk=None):
        card_pk = pk
        data=request.data
        card_status=data['status']
        card_info = Card.objects.get(pk=card_pk)
        card_info.status=card_status
        card_info.save()
        return Response(Card_Serializer.CardAssigneeSerializer(card_info).data,status=status.HTTP_200_OK)