# Generated by Django 3.1.7 on 2021-04-12 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media', models.FileField(null=True, upload_to=post.models.get_user_directory)),
                ('post_id', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, null=True)),
                ('caption', models.CharField(blank=True, max_length=280)),
                ('status', models.CharField(choices=[('Drafts', 'Drafts'), ('Published', 'Published')], default='Draft', max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('multimedia', models.ManyToManyField(blank=True, related_name='Post', to='post.Media')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Post_team', to='team.team')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(blank=True, max_length=280)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.post')),
            ],
        ),
    ]
