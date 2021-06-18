from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as template_serializer
from .models import Template
from team.models import Team
from .reciever_retrieval import recieve_mail_list
from .NotificationSender import Instance as notification_sender
from scheduler.scheduler import Instance as scheduler
import datetime
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
        template_name=data['name']
        reciviers = data['reciviers']
        sender=data['sender']
        template_team=Team.objects.get(pk=data['template_team'])
        template_status=data['status']
        #TODO recieve schedule time and subject
        temp=Template.objects.create(name=template_name,reciviers=reciviers,sender=sender,template_team=template_team,status=template_status)
        
        emails=recieve_mail_list(reciviers)

        #get variables in api
        api_vars=[]
        print(reciviers)
        if len(emails)>0:
            api_vars = list(emails[0].keys())
        
        if 'body_text' in data:
            temp.body_text = data['body_text']

            #check for the variables
            if len(api_vars)>0: 
                for var in api_vars:
                    if var=='email':
                        continue
                    if not temp.body_text.__contains__(f'%^{var}^%'):
                        return Response(data=var,status=status.HTTP_406_NOT_ACCEPTABLE)
                        # "Variable {var} that you have provided don't exist in your given API."

        if 'subject' in data:
            temp.subject = data['subject']

        if temp.status=='Send':
            for e in emails:
                notification_sender.send_mail(temp, e)

        if temp.status=='Schedule':
            #replace variables 
            scheduler.schedule_mail(temp, datetime.datetime.now() + datetime.datetime(0, 0, 0, 0, 2)) #TODO recieve shcedule time

        return Response(template_serializer.TemplateSerializer(temp).data, status=status.HTTP_201_CREATED)