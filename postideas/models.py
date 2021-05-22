from django.db import models
from users.models import User
from team.models import Team

class Card(models.Model):

    tag_CHOICES = (
        ('Low priority','Low priority'),
        ('High priority','High priority'),
        ('Medium priority','Medium priority'),
    )
    
    title = models.CharField(null = True, max_length=60)
    description = models.CharField(blank = True, max_length=280)
    status = models.CharField(null = True, max_length=60)
    assignee = models.ForeignKey(User, related_name = 'assignee', blank = True,null=True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    team = models.ForeignKey(Team, related_name = 'workspace', null = True, on_delete = models.CASCADE)
    tag = models.CharField(blank = True, null=True,max_length=20,choices = tag_CHOICES)
    

