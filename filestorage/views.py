from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import MediaStorage
from users.models import User
from team.models import Team
from . import serializers as MediaStorage_serializer

class UploadFileView(generics.CreateAPIView):
    queryset = FileStorage.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaStorage_serializer.FileSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        file_titile=data['title']
        file_media=data['media']
        f = FileStorage(title=file_titile)
        f.save()
        f.media = file_media
        f.save()
        return Response(MediaStorage_serializer.FileSerializer(f).data, status=status.HTTP_201_CREATED)


class SingleFileView(generics.RetrieveAPIView):
    queryset = FileStorage.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaStorage_serializer.FileSerializer

    def get(self, request, pk=None):
        file_Info = FileStorage.objects.all().get(pk=pk)
        serializer = MediaStorage_serializer.FileSerializer(file_Info)
        return Response(serializer.data, status=status.HTTP_200_OK)