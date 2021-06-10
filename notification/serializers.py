from rest_framework import serializers
from . import models

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = ('id','name', 'body_text', 'subject', 'reciviers','sender','template_team','created_at','schedule_time','status')
    read_only_fields = ('id')
