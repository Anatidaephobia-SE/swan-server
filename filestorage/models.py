from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix

priv_bucket = "django-backend-dev-private"

class MediaStorage(models.Model):
    title = models.CharField(max_length=255)
    media = models.FileField(verbose_name="Object Upload",
                            storage=MinioBackend(bucket_name=priv_bucket),
                            upload_to=iso_date_prefix)

    def __str__(self):
        return self.title