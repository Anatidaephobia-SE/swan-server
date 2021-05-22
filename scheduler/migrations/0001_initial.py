# Generated by Django 3.1.7 on 2021-05-22 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.IntegerField()),
                ('body', models.TextField(max_length=10000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('scheduled_date', models.DateTimeField()),
                ('state', models.IntegerField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]
