from rest_framework import serializers




class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=50)
    balance = serializers.IntegerField(default=0)
    creation_datetime = serializers.DateTimeField()

class UserRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    room = RoomSerializer()
    creation_datetime = serializers.DateTimeField()

class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    users = UserSerializer(many=True)
    creation_datetime = serializers.DateTimeField()
    money = serializers.IntegerField()
    