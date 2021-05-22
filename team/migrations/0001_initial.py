# Generated by Django 3.1.7 on 2021-05-22 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import team.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100, unique=True)),
                ('logo', models.ImageField(null=True, upload_to=team.models.get_teamlogo_directory)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('pending_users', models.ManyToManyField(blank=True, related_name='pending_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
