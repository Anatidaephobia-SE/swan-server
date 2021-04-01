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
        data['owner'] = user.email
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post = serializer.save()
        for m in data['multimedia']:
            i = Media.objects.create(media=m['media'])
            post.multimedia.add(i)
        return Response("Post created!", status=status.HTTP_202_ACCEPTED)

class UpdatePostView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.PostSerializer

    def get(self, request, pk=None):
        user = request.user
        post_info = Post.objects.all().get(pk=pk)
        posts_query = user.Post_owner.all()
        if not posts_query.filter(pk=pk).exists():
            return Response("This post does not exist!", status=status.HTTP_400_BAD_REQUEST)
        serializer = post_serializer.PostSerializer(post_info)
        serializer.data['owner'] = User.objects.get(email=serializer.data['owner'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        post_info = Post.objects.all().get(pk=pk)
        posts_query = user.Post_owner.all()
        if not posts_query.filter(pk=pk).exists():
            return Response("This post does not exist!", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=post_info, data=data)
        if serializer.is_valid(True):
            post = serializer.update(instance=post_info, validated_data=serializer.validated_data)
                
            post.multimedia.clear()
            for m in data['multimedia']:
                i = Media.objects.create(media=m['media'])
                post.multimedia.add(i)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        post_info = Post.objects.all().get(pk=pk)
        posts_query = user.Post_owner.all()
        if not posts_query.filter(pk=pk).exists():
            return Response("This post does not exist!", status=status.HTTP_400_BAD_REQUEST)
        multimedia_info = post_info.multimedia.all()
        for i in multimedia_info:
            i.delete()
        post_info.delete()
        return Response("OK", status=status.HTTP_202_ACCEPTED)

class SinglePostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.PostSerializer

    def get(self, request, pk=None):
        post_Info = Post.objects.all().get(pk=pk)
        serializer = post_serializer.PostSerializer(post_Info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)