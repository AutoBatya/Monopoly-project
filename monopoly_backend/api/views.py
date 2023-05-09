from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import models

from .models import Room
from .serializers import RoomSerializer


from datetime import datetime
# Create your views here.


class GetAllRooms(APIView):
    def get(self, request):
        queryset = Room.objects.all()
        serializer = RoomSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)


class GetRoomById(APIView):
    def get(self, request, id):
        queryset = Room.objects.filter(id=id)
        if queryset.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(
            instance=queryset[0],
            many=False
        )
        return Response(serializer.data)

class CreateRoom(APIView):
    def get(self, request):
        name = request.GET.get("name")
        max_players = request.GET.get("max_players")
        starting_balance = request.GET.get("starting_balance")

        if name is None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        if max_players is None:
            max_players = 4
        else:
            if not max_players.isdigit():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                max_players = int(max_players)

        if starting_balance is None:
            starting_balance = 0
        else:
            if not starting_balance.isdigit():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                starting_balance = int(starting_balance)

        queryset = Room.objects.filter(name=name)
        if len(queryset) != 0:
            return Response(status=status.HTTP_409_CONFLICT)

        room = Room()
        room.name = name
        room.max_players = max_players
        room.current_players = 0
        room.starting_balance = starting_balance
        room.creation_datetime = datetime.now()
        room.save()

        queryset = Room.objects.filter(name=name)
        serializer = RoomSerializer(
            instance=queryset[0],
            many=False
        )

        return Response(serializer.data, status=status.HTTP_200_OK)