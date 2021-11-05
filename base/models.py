from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



class User_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", default="avatar.svg", blank=True, null=True)
    bio = models.CharField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)

class Topic(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.name)

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)


    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return str(self.body[0:50])

