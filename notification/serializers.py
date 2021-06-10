from rest_framework import serializers
from . import models

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = ('id','template_name', 'body_text', 'subject', 'reciviers','sender','created_at','schedule_time')
    read_only_fields = ('id')
