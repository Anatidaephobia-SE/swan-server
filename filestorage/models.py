from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix
from team.models import Team
from users.models import User

priv_bucket = "django-backend-dev-private"


def iso_date_prefix(instance,file_name_ext: str) -> str:
    return f"{instance.team}/{file_name_ext}"

class MediaStorage(models.Model):
    team = models.ForeignKey(Team, related_name = 'storage_team', null = True, on_delete = models.CASCADE)
    owner = models.ForeignKey(User, related_name = 'media_owner', null=True, on_delete = models.CASCADE)
    media = models.FileField(verbose_name="Object Upload",
                            storage=MinioBackend(bucket_name=priv_bucket),
                            upload_to=iso_date_prefix)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.media.delete()
        super(MediaStorage, self).delete(*args, **kwargs)