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