from postideas.models import Card
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as Card_Serializer
from users.models import User
from team.models import Team

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
        card_tag = data['tag']
        card = Card(team=card_workspace,title=card_title,description=card_description,status=card_status,assignee=user,tag=card_tag)
        card.save()
        post_files=request.FILES.getlist('multimedia[]')
        return Response(Card_Serializer.CardSerializer(card).data, status=status.HTTP_201_CREATED)
 
