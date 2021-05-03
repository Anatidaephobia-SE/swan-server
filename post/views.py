from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from . import serializers as post_serializer
from .models import Post, Media, Comment
from users.models import User
from team.models import Team
from socialmedia.models import SocialMedia
from socialmedia.twitter import Tweet
from scheduler.scheduler import Scheduler
from scheduler.models import TaskType
from datetime import datetime
class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.PostSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post_team=Team.objects.get(pk=data['team'])
        post_name=data['name']
        post_caption=data['caption']
        post_status=data['status']
        post = Post(team=post_team,name=post_name,caption=post_caption,status=post_status,owner=user)
        post.save()
        post_files=request.FILES.getlist('multimedia[]')
        for media_file in post_files:
            media = Media.objects.create(media=media_file, post_id = post.id)
            post.multimedia.add(media)
        return Response(post_serializer.PostSerializer(post).data, status=status.HTTP_201_CREATED)

class UpdatePostView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.UpdatePostSerializer

    def get(self, request, pk=None):
        user = request.user
        post_info = Post.objects.all().get(pk=pk)
        posts_query = user.owner.all()
        if not posts_query.filter(pk=pk).exists():
            return Response("You did not create this post!", status=status.HTTP_400_BAD_REQUEST)
        serializer = post_serializer.UpdatePostSerializer(post_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        post_info = Post.objects.all().get(pk=pk)
        posts_query = user.owner.all()
        teams_query = Team.objects.all()
        if not posts_query.filter(pk=pk).exists():
            return Response("You did not create this post!", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=post_info, data=data)

        if serializer.is_valid(True):
            post = serializer.update(instance=post_info, validated_data=serializer.validated_data)    
            post_files=request.FILES.getlist('multimedia[]')
            if len(post_files) != 0:
                post.multimedia.clear()
            for media_file in post_files:
                media = Media.objects.create(media=media_file, post_id = post.id)
                post.multimedia.add(media)
                
            if post.status == 'Published':
                socialmedia=SocialMedia.objects.all().get(team=post.team)
                # twitter_response = Tweet(post,socialmedia)
                sc = Scheduler()
                sc.schedule(post, socialmedia, TaskType.Twitter, datetime.now())
                return Response(data={"message": "added to tyhe queue"},status=status.HTTP_200_OK)
                if twitter_response.status_code != 200 :
                    post.status == 'Error'
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response("Bad request.", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        post_info = Post.objects.all().get(pk=pk)
        posts_query = user.owner.all()
        if not posts_query.filter(pk=pk).exists():
            return Response("You did not create this post.", status=status.HTTP_400_BAD_REQUEST)
        multimedia_info = post_info.multimedia.all()
        for i in multimedia_info:
            i.delete()
        post_info.delete()
        return Response("Post deleted.", status=status.HTTP_200_OK)

class SinglePostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.PostSerializer

    def get(self, request, pk=None):
        post_Info = Post.objects.all().get(pk=pk)
        serializer = post_serializer.PostSerializer(post_Info)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.PostSerializer

    def get(self, request, pk=None):
        postsList = Post.objects.all().filter(team=pk)
        serializer = post_serializer.PostSerializer(postsList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateCommentView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.CommentSerializer
    def put(self, request, pk=None):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        comment_context=data['context']
        comment_post=Post.objects.get(pk=pk)
        comment = Comment(author=user,context=comment_context,post=comment_post)
        comment.save()
        return Response(post_serializer.CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    
class AllCommentsView(generics.ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.CommentSerializer
    pagination_class = PageNumberPagination
    def get(self, request, pk=None):
        commentsList = Comment.objects.all().filter(post=pk)
        serializer = post_serializer.CommentSerializer(commentsList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteCommentView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = post_serializer.CommentSerializer
    def delete(self, request, pk=None):
        user = request.user
        comment_info = Comment.objects.all().get(pk=pk)
        comments_query = user.comment_author.all()
        if not comments_query.filter(pk=pk).exists():
            return Response("You did not write this comment.", status=status.HTTP_400_BAD_REQUEST)
        comment_info.delete()
        return Response("Comment deleted.", status=status.HTTP_200_OK)