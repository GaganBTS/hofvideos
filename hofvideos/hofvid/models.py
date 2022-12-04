from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
# Create your models here.
class Hall(models.Model):
    title = models.CharField(max_length=300)
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}'

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=255)
    url = models.URLField(max_length=400)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}, {self.hall}'
