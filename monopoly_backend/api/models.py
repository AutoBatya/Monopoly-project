from django.db import models


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=50)
    max_players = models.IntegerField(default=4)
    current_players = models.IntegerField()
    starting_balance = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField()

class Transaction(models.Model):
    users = models.ManyToManyField(User)
    creation_datetime = models.DateTimeField(null=True)
    money =models.IntegerField(null=True)
    
    

