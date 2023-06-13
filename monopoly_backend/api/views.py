from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import models

from .models import Room, User, UserRoom, Transaction
from .serializers import RoomSerializer, UserSerializer, UserRoomSerializer, TransactionSerializer

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from datetime import datetime


# Create your views here.


class GetAllRooms(APIView):
    def get(self, request):
        queryset = Room.objects.all()
        serializer = RoomSerializer(
            instance=queryset,
            many=True
        )
        return JsonResponse(serializer.data, safe=False)


class GetRoomById(APIView):
    def get(self, request, id):
        queryset = Room.objects.filter(id=id)
        if queryset.count() == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)

        serializer = RoomSerializer(
            instance=queryset[0],
            many=False
        )
        return JsonResponse(serializer.data, safe=False)


class CreateRoom(APIView):
    def get(self, request):
        name = request.GET.get("name")
        max_players = request.GET.get("max_players")
        starting_balance = request.GET.get("starting_balance")

        if name is None:
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)

        if max_players is None:
            max_players = 4
        else:
            if not max_players.isdigit():
                return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
            else:
                max_players = int(max_players)

        if starting_balance is None:
            starting_balance = 0
        else:
            if not starting_balance.isdigit():
                return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
            else:
                starting_balance = int(starting_balance)

        queryset = Room.objects.filter(name=name)
        if len(queryset) != 0:
            return JsonResponse({}, status=status.HTTP_409_CONFLICT, safe=False)

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

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

class GetUsersByIdRoom(APIView):
    def get(self, request, id_room):
        queryset = UserRoom.objects.filter(room_id=id_room)
        if len(queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)
        user_queryset = User.objects.filter(id__in=[userroom.user_id for userroom in queryset])
        serializer = UserSerializer(
            instance=user_queryset,
            many=True
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class MoneyTransfer(APIView):
    def get(self, request):
        money = request.GET.get("money")
        sender = request.GET.get("sender_id")
        receiver = request.GET.get("receiver_id")
        if sender is None or receiver is None or not sender.isdigit() or not receiver.isdigit() or money is None or not money.isdigit():
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
        if sender == receiver:
            return JsonResponse({}, status=status.HTTP_409_CONFLICT, safe=False)
        sender = User.objects.filter(id=int(sender))
        receiver = User.objects.filter(id=int(receiver))
        money = int(money)
        if len(sender) != 1 or len(receiver) != 1:
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
        sender = sender[0]
        receiver = receiver[0]
        if sender.balance - money < 0:
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
        sender.balance -= money
        receiver.balance += money
        sender.save()
        receiver.save()
        transaction = Transaction()
        transaction.save()
        transaction.users.add(sender, receiver)
        transaction.creation_datetime = datetime.now()
        transaction.money = money
        transaction.save()
        serializer = TransactionSerializer(
            instance=transaction,
            many=False
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)



