from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import models

from .models import Room, User, UserRoom, Transaction, Activity
from .serializers import RoomSerializer, UserSerializer, UserRoomSerializer, TransactionSerializer, ActivitySerializer

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from datetime import datetime

import json

from django.http import HttpResponse

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


class CreateUser(APIView):
    def get(self, request):
        id_room = request.GET.get("id_room")
        username = request.GET.get("username")
        balance = request.GET.get("balance")
        if id_room is None or username is None:
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
        if not id_room.isdigit():
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
        else:
            id_room = int(id_room)
        room_queryset = Room.objects.filter(id=id_room)
        if len(room_queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)
        room = room_queryset[0]
        if room.max_players < room.current_players + 1:
            return JsonResponse({}, status=status.HTTP_409_CONFLICT, safe=False)

        if balance is None:
            balance = room_queryset[0].starting_balance
        else:
            if not balance.isdigit():
                return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)
            else:
                balance = int(balance)

        user_queryset = User.objects.filter(username=username)
        if len(user_queryset) > 0:
            user = user_queryset[0]
            user_room_queryset = UserRoom.objects.filter(user__in=user_queryset).filter(room=room)
            if len(user_room_queryset) > 0:
                return JsonResponse({}, status=status.HTTP_409_CONFLICT, safe=False)

        user = User()
        user.username = username
        user.balance = balance
        user.creation_datetime = datetime.now()
        user.save()

        user_room = UserRoom()
        user_room.user = user
        user_room.room = room
        user_room.creation_datetime = datetime.now()

        room.current_players += 1
        room.save()

        user_room.save()

        serializer = UserRoomSerializer(
            instance=user_room,
            many=False
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class GetUserByIdRoom(APIView):
    def get(self, request, id_user, id_room):
        user_queryset = User.objects.filter(id=id_user)
        room_queryset = Room.objects.filter(id=id_room)
        if len(user_queryset) == 0 or len(room_queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)

        user_room_queryset = UserRoom.objects.filter(user=user_queryset[0]).filter(room=room_queryset[0])
        if len(user_room_queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)

        serializer = UserSerializer(
            instance=user_queryset[0],
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



class CountPlayers(APIView):
    def get(self, request):
        id_room = request.GET.get("id_room")

        if id_room is None or not id_room.isdigit():
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)

        id_room = int(id_room)
        
        room_queryset = Room.objects.filter(id=id_room)
        if len(room_queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)

        userroom_queryset = UserRoom.objects.filter(room=id_room)
        return JsonResponse(len(userroom_queryset), status=status.HTTP_200_OK, safe=False)


class ListActivity(APIView):
    def get(self, request):
        id_room = request.GET.get("id_room")
        id_user = request.GET.get("id_user")

        if id_room is None or id_user is None or not id_room.isdigit() or not id_user.isdigit():
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)

        userroom_queryset = UserRoom.objects.filter(room=id_room).filter(user=id_user)
        if len(userroom_queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

        transaction_queryset = Transaction.objects.filter(users__id=id_user)
        activities_queryset = Activity.objects.filter(user=id_user)

        transaction_serializer = TransactionSerializer(
            instance=transaction_queryset,
            many=True
        )

        activities_serializer = ActivitySerializer(
            instance=activities_queryset,
            many=True
        )

        result = {"Transactions": json.loads(json.dumps(transaction_serializer.data)), "Activities": json.loads(json.dumps(activities_serializer.data))}

        return JsonResponse(result, status=status.HTTP_200_OK, safe=False)

    
    
class GetTransactionsByRoomID(APIView):
    def get(self, request, id_room):
        queryset = UserRoom.objects.filter(room_id=id_room)
        if len(queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)
        
        transaction_queryset = Transaction.objects.filter(id__in=[userroom.room_id for userroom in queryset])
        serializer = TransactionSerializer(
            instance=transaction_queryset,
            many=True
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class GetTransactionsByUserID(APIView):
    def get(self, request, id_user):
        queryset = UserRoom.objects.filter(user_id=id_user)
        if len(queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)
        transaction_queryset = Transaction.objects.filter(id__in=[userroom.user_id for userroom in queryset])
        serializer = TransactionSerializer(
            instance=transaction_queryset,
            many=True
        )
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

def request_money(request):
    if request.method == 'POST':
        player = request.POST.get('player')
        amount = request.POST.get('amount')
        # Do something with player and amount
        return HttpResponse('Money requested from player {} for amount {}'.format(player, amount))
    else:
        return HttpResponse('Invalid request method')

def approve_money_request(request):
    if request.method == 'POST':
        player = request.POST.get('player')
        amount = request.POST.get('amount')
        approved = request.POST.get('approved')
        # Do something with player, amount and approved
        return HttpResponse('Money request from player {} for amount {} was {}'.format(player, amount, approved))
    else:
        return HttpResponse('Invalid request method')
