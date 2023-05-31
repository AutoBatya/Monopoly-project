from django.db import models


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=50)
    max_players = models.IntegerField(default=4)
    current_players = models.IntegerField()
    starting_balance = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField()


class User(models.Model):
    username = models.CharField(max_length=50)
    user_id = models.IntegerField()
    balance = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField()


class UserRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_datetime = models.DateTimeField(null=True)
    

class Transaction(models.Model):
    users = models.ManyToManyField(User, null=True)
    creation_datetime = models.DateTimeField(null=True)
    money =models.IntegerField(null=True)
    
    
class Action(models.Model):
    type_action = models.CharField(max_length=255)
    user_id = models.IntegerField()
    room_id = models.IntegerField()
    action_time = models.DateTimeField()
