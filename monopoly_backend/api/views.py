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
from random import randint


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



class Dice(APIView):
    def get(self, request):
        dice1, dice2 = randint(1, 6), randint(1, 6)
        answer = {
            "dice1": dice1,
            "dice2": dice2,
            "sum": dice1 + dice2
        }
        return JsonResponse(answer, status=status.HTTP_200_OK, safe=False)

class DiceRate(APIView):
    EVEN, ODD = "even", "odd"
    def get(self, request):
        def check(a, b):
            if a == DiceRate.EVEN and b % 2 == 0 \
                    or a == DiceRate.ODD and b % 2 != 0:
                return True
            else:
                return False

        user_id = request.GET.get("user_id")
        rate = request.GET.get("rate")
        bet = request.GET.get("bet") #even or odd
        print(user_id, rate, bet)
        if user_id is None or rate is None or bet is None \
                or not rate.isdigit() or not user_id.isdigit() \
                or not (bet in [DiceRate.EVEN, DiceRate.ODD]):
            return JsonResponse({}, status=status.HTTP_406_NOT_ACCEPTABLE, safe=False)

        user_id = int(user_id)
        rate = int(rate)

        user_queryset = User.objects.filter(id=user_id)

        if len(user_queryset) == 0:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND, safe=False)

        user = user_queryset[0]

        if rate > user.balance:
            return JsonResponse({"error": "not_enough_money"})

        dice1, dice2 = randint(1, 6), randint(1, 6)
        _sum = dice1 + dice2
        answer = {
            "dice1": dice1,
            "dice2": dice2,
            "sum": dice1 + dice2
        }

        if check(bet, _sum):
            user.balance += rate
            user.save()
            return JsonResponse(answer | {"status": "win"})
        else:
            user.balance -= rate
            user.save()
            return JsonResponse(answer | {"status": "lose"})

class GetActionsByUserId(APIView):
    def get_actions(request):
        room_id = request.GET.get('room_id')
        user_token = request.GET.get('user_token')
        last_action_id = request.GET.get('last_action_id')
        if not room_id or not user_token:
            return JsonResponse({'error': 'Не указаны id комнаты или токен пользователя'})
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Комната с указанным id не найдена'})
        if not room.user_set.filter(token=user_token).exists():
            return JsonResponse({'error': 'Пользователь не имеет доступа к данной комнате'})
        if last_action_id:
            try:
                last_action = room.action_set.get(id=last_action_id)
            except Action.DoesNotExist:
                return JsonResponse({'error': 'Указанный id последнего известного действия не найден'})
            actions = room.action_set.filter(id__gt=last_action_id)
        else:
            actions = room.action_set.all()
        serializer = RoomSerializer(actions, many=True)

        return JsonResponse(serializer.data, safe=False)
