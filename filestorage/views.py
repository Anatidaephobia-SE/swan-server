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

    def get(self, request):
        
        req_check = have_queryparams(request, 'media_pk')

        if not req_check.have_all:
            return Response({'error': req_check.error_message}, status=status.HTTP_400_BAD_REQUEST)
        media_pk = request.query_params.get("media_pk")

        file_Info = FileStorage.objects.all().get(pk=media_pk)
        serializer = MediaStorage_serializer.FileSerializer(file_Info)
        return Response(serializer.data, status=status.HTTP_200_OK)