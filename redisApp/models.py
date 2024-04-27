from django.db import models
from django.contrib.auth.models import User


class group_chat_message(models.Model):
    _id=models.AutoField(primary_key=True,unique=True)
    group_name=models.TextField()
    current_user=models.CharField(max_length=100)
    created_time=models.DateTimeField(auto_now_add=True)
    msg=models.TextField()
    def __str__(self):
       return self.group_name
