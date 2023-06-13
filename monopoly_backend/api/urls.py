from django.urls import path

from . import views

urlpatterns = [
    path("api/rooms/", views.GetAllRooms.as_view()),
    path("api/rooms/<int:id>/", views.GetRoomById.as_view()),
    path("api/rooms/create/", views.CreateRoom().as_view()),
    path("api/users/rooms/<int:id_room>", views.GetUsersByIdRoom().as_view()),
    path("api/users/send/", views.MoneyTransfer().as_view())

]