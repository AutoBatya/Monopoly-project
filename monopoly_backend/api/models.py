from django.db import models


# Create your models here.



class User(models.Model):
    username = models.CharField(max_length=50)
    balance = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField()


class UserRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_datetime = models.DateTimeField(null=True)
    

class Transaction(models.Model):
    users = models.ManyToManyField(User)
    creation_datetime = models.DateTimeField(null=True)
    money =models.IntegerField(null=True)
    
    

