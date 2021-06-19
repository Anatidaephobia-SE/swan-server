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
        temp=Template.objects.create(name=template_name,reciviers=reciviers,sender=sender,template_team=template_team,status=template_status,owner=user)

        
        emails=recieve_mail_list(reciviers)

        #get variables in api
        api_vars=[]
        if len(emails)>0:
            api_vars = list(emails[0].keys())
        
        if 'body_text' in data:
            temp.body_text = data['body_text']
            temp.save()

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

        temp.save()
        if temp.status=='Send':
            for e in emails:
                notification_sender.send_mail(temp, e)

        if temp.status=='Schedule':
            #replace variables 
            temp.schedule_time = data['schedule_time']
            temp.save()
            scheduler.schedule_mail(temp, datetime.datetime.now()) 


        return Response(template_serializer.TemplateSerializer(temp).data, status=status.HTTP_201_CREATED)


class UpdateTemplateView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = template_serializer.UpdateTemplateSerializer

    def get(self, request, pk=None):
        user = request.user
        template_info = Template.objects.all().get(pk=pk)
        templates_query = user.template_owner.all()
        if not templates_query.filter(pk=pk).exists():
            return Response("You did not create this template!", status=status.HTTP_400_BAD_REQUEST)
        serializer = template_serializer.UpdateTemplateSerializer(template_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        user = request.user
        data = request.data
        template_info = Template.objects.all().get(pk=pk)
        templates_query = user.template_owner.all()
        if not templates_query.filter(pk=pk).exists():
            return Response("You did not create this template!", status=status.HTTP_400_BAD_REQUEST)
        print(data)
        serializer = self.get_serializer(instance=template_info, data=data)
        print(serializer.is_valid(True))
        #raise_exception=
        if serializer.is_valid(True):
            temp = serializer.update(instance=template_info, validated_data=serializer.validated_data)  

            emails=recieve_mail_list(temp.reciviers)
            #get variables in api
            api_vars=[]
            if len(emails)>0:
                api_vars = list(emails[0].keys())

            if temp.status == 'Send':
                
                for e in emails:
                    #replace variables 
                    email_text=""
                    for var in api_vars:
                        if var=='email':
                            continue
                        email_text = temp.body_text.replace(f'%^{var}^%',e[f'{var}'])
                    #send_email(email_text,body_text,...)
                # temp.schedule_time = datetime.now()
                # temp.save()

            if temp.status == 'Schedule':
                #replace variables 
                for e in emails:
                    email_text=""
                    for var in api_vars:
                        if var=='email':
                            continue
                        email_text = temp.body_text.replace(f'%^{var}^%',e[f'{var}'])
                    #Schedule_email(email_text,body_text,...)
                temp.schedule_time = data['schedule_time']
                # temp.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
             
 
        print("*******************************************************************",serializer.errors)  
        return Response("Bad request.", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        template_info = Template.objects.all().get(pk=pk)
        templates_query = user.template_owner.all()
        if not templates_query.filter(pk=pk).exists():
            return Response("You did not create this template.", status=status.HTTP_400_BAD_REQUEST)
        template_info.delete()
        return Response("templatet deleted.", status=status.HTTP_200_OK)

class SingleTemplateView(generics.RetrieveAPIView):
    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = template_serializer.UpdateTemplateSerializer

    def get(self, request, pk=None):
        template_Info = Template.objects.all().get(pk=pk)
        serializer =  template_serializer.UpdateTemplateSerializer(template_Info)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllTemplateView(generics.ListAPIView):
    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = template_serializer.UpdateTemplateSerializer

    def get(self, request, pk=None):
        templatesList = Template.objects.all().filter(template_team=pk)
        serializer =  template_serializer.UpdateTemplateSerializer(templatesList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)