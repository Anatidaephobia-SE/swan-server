# Generated by Django 3.1.7 on 2021-04-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]