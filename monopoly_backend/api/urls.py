from django.urls import path

from . import views

urlpatterns = [
    path("api/rooms/", views.GetAllRooms.as_view()),
    path("api/rooms/<int:id>/", views.GetRoomById.as_view()),
    path("api/rooms/create/", views.CreateRoom().as_view()),
    path("api/users/create/", views.CreateUser().as_view()),
    path("api/users/<int:id_user>/rooms/<int:id_room>/", views.GetUserByIdRoom().as_view()),
    path("api/users/rooms/<int:id_room>/", views.GetUsersByIdRoom().as_view()),
    path("api/users/send/", views.MoneyTransfer().as_view()),
    path("api/users/count/", views.CountPlayers().as_view()),
    path('request-money/', views.request_money, name='request-money'),
    path('approve-money-request/', views.approve_money_request, name='approve-money-request'),

]
