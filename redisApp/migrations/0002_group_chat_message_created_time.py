# Generated by Django 5.0.4 on 2024-04-25 18:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redisApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_chat_message',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
