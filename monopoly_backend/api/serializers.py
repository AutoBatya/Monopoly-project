from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    max_players = serializers.IntegerField(default=4)
    current_players = serializers.IntegerField()
    starting_balance = serializers.IntegerField(default=0)
    creation_datetime = serializers.DateTimeField()

class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    users = UserSerializer(many=True)
    creation_datetime = serializers.DateTimeField()
    money = serializers.IntegerField()
    

