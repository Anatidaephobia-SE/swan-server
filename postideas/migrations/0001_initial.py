# Generated by Django 3.1.7 on 2021-05-20 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, null=True)),
                ('description', models.CharField(blank=True, max_length=280)),
                ('status', models.CharField(max_length=60, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(blank=True, choices=[('Low priority', 'Low priority'), ('High priority', 'High priority'), ('Medium priority', 'Medium priority')], max_length=20)),
                ('assignee', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workspace', to='team.team')),
            ],
        ),
    ]