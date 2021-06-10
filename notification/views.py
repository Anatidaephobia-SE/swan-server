from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as template_serializer
from .models import Template
from users.models import User
from team.models import Team
from socialmedia.models import SocialMedia
from socialmedia.twitter import Tweet
from scheduler.scheduler import Scheduler
from scheduler.models import TaskType
from datetime import datetime
from filestorage.models import MediaStorage

class CreateTemplatetView(generics.CreateAPIView):
    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = template_serializer.TemplateSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #fields = ('id','template_name', 'body_text', 'subject', 'reciviers','sender','created_at','schedule_time')
        template_name=data['template_name']
        reciviers = data['reciviers']
        sender=data['sender']
        template_team=Team.objects.get(pk=data['template_team'])
        temp=Template.objects.create(template_name=template_name,reciviers=reciviers,sender=sender,template_team=template_team)

        if 'body_text' in data:
            temp.body_text = data['body_text']
        if 'subject' in data:
            temp.subject = data['subject']

        # if post.status == 'Published':
        #     socialmedia=SocialMedia.objects.all().get(team=post.team)
        #     twitter_response, published_id = Tweet(post,socialmedia)
        #     post.published_id=published_id
        #     post.schedule_time = datetime.now()
        #     post.save()
        #     if twitter_response.status_code != 200 :
        #         return Response("An Error has occured during publishing")
        # if post.status == 'Schedule':
        #     sc = Scheduler()
        #     socialmedia=SocialMedia.objects.all().get(team=post.team)
        #     if 'schedule_time' in data:
        #         sc.schedule_post(post, socialmedia, TaskType.Twitter, data['schedule_time'])
        #         post.schedule_time=data['schedule_time']
        #         post.save()
        #         return Response(data={"message": "added to the queue", "date": sc.get_post_scheduled_date(post, TaskType.Twitter)},status=status.HTTP_200_OK)
        return Response(template_serializer.PostSerializer(temp).data, status=status.HTTP_201_CREATED)