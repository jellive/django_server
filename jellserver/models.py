from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=127)
    context = models.CharField(max_length=65535)
    writer = models.CharField(max_length=128)
    cdatetime = models.DateTimeField(auto_now=True)
    udatetime = models.DateTimeField(auto_now=True)
