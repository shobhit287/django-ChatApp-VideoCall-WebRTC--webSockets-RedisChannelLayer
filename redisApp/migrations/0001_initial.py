# Generated by Django 5.0.4 on 2024-04-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='group_chat_message',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('group_name', models.TextField()),
                ('channel_layer', models.TextField()),
                ('msg', models.TextField()),
            ],
        ),
    ]
