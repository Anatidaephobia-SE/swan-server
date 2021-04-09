# Generated by Django 3.1.7 on 2021-04-03 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0002_auto_20210319_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_oauth_token', models.TextField(max_length=200, null=True)),
                ('twitter_oauth_token_secret', models.TextField(max_length=200, null=True)),
                ('twitter_user_id', models.TextField(max_length=200, null=True)),
                ('twitter_name', models.TextField(max_length=200, null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
        ),
    ]
