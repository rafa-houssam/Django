from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.TextField(null=True)
    avatar=models.ImageField(null=True,default='avatar.svg')
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

# # Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    description=models.TextField(null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering=['-updated','-created']
    

class Message(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:50]
