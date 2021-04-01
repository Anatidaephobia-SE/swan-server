from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as post_serializer
from .models import Post, Media
from users.models import User


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.PostSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['owner'] = user.id
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post = serializer.save()
        for m in data['multimedia']:
            i = Media.objects.create(media=m['media'])
            post.multimedia.add(i)
        return Response("OK", status=status.HTTP_202_ACCEPTED)