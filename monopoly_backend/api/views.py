from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import models

from .models import Room
from .serializers import RoomSerializer

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