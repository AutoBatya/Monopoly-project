from django.urls import path

from . import views

urlpatterns = [
    path("api/rooms/", views.GetAllRooms.as_view()),
    path("api/rooms/<int:id>/", views.GetRoomById.as_view()),
]