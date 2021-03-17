from django.db import models

def get_teamlogo_directory(instance, filename):
    return f'uploads/teamlogo/{instance.url}/{filename}'


class team(models.Model):
    name = models.CharField(max_length = 100)
    url = models.CharField(primary_key = True, max_length = 100)
    logo = models.ImageField(upload_to = get_teamlogo_directory, null = True)
    users = models.ManyToManyField('users.User', related_name = 'users')
    head = models.ForeignKey('users.User', related_name = 'head', on_delete = models.CASCADE, null = True) # temparary
    created_at = models.DateField(auto_now_add = True)