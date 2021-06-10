from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers as template_serializer
from .models import Template
from team.models import Team
from .reciever_retrieval import recieve_mail_list

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
        temp=Template.objects.create(name=template_name,reciviers=reciviers,sender=sender,template_team=template_team,status=template_status)

        if 'body_text' in data:
            temp.body_text = data['body_text']
        if 'subject' in data:
            temp.subject = data['subject']
        if temp.status=='Send':
            emails=recieve_mail_list(reciviers)
            print(emails)
            #for e in emails:
                #send_email(temp_subject,body_text,...)
        return Response(template_serializer.TemplateSerializer(temp).data, status=status.HTTP_201_CREATED)