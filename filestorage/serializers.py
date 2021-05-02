from rest_framework import serializers
from . import models

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MediaStorage
        fields = ('id','title','media')