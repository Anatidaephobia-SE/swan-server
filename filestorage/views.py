from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import MediaStorage
from users.models import User
from team.models import Team
from . import serializers as FileStorage_serializer
from request_checker.functions import *

from swan.settings import MINIO_ENDPOINT
import os


class UploadFileView(generics.CreateAPIView):
    queryset = MediaStorage.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FileStorage_serializer.FileSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        file_media=data['media']
        file_team=Team.objects.get(pk=data['team'])
        f = MediaStorage(team=file_team,owner=user)
        f.save()
        f.media = file_media
        f.save()
        response = FileStorage_serializer.FileSerializer(f).data
        return Response(response, status=status.HTTP_201_CREATED)


class SingleFileView(generics.RetrieveAPIView):
    queryset = MediaStorage.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FileStorage_serializer.FileSerializer

    def get(self, request):
        
        req_check = have_queryparams(request, 'media_pk')

        if not req_check.have_all:
            return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
        media_pk = request.query_params.get("media_pk")

        file_Info = MediaStorage.objects.all().get(pk=media_pk)
        serializer = FileStorage_serializer.FileSerializer(file_Info)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllMediaView(generics.ListAPIView):
    queryset = MediaStorage.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FileStorage_serializer.FileSerializer

    def get(self, request):

        req_check = have_queryparams(request, 'team_id')

        if not req_check.have_all:
            return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
        team_id = request.query_params.get("team_id")

        mediaList = MediaStorage.objects.all().filter(team=team_id)
        serializer = FileStorage_serializer.FileSerializer(mediaList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteMediaView(generics.DestroyAPIView):

    queryset = MediaStorage.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FileStorage_serializer.FileSerializer

    def delete(self, request):

        req_check = have_queryparams(request, 'media_pk')

        if not req_check.have_all:
            return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
        media_pk = request.query_params.get("media_pk")

        user = request.user
        media_info = MediaStorage.objects.get(pk=media_pk)
        medias_query = user.media_owner.all()

        if user==media_info.team.head: #head of team can delete the uploaded media
             media_info.delete()
             return Response("File deleted.", status=status.HTTP_200_OK)

        if not medias_query.filter(pk=media_pk).exists():
            return Response("You did not upload this file.", status=status.HTTP_400_BAD_REQUEST)

        media_info.delete()
        return Response("File deleted.", status=status.HTTP_200_OK)
