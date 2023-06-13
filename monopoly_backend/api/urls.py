from django.urls import path

from . import views

urlpatterns = [
    path("api/users/create/", views.CreateUser().as_view()),
    path("api/users/<int:id_user>/rooms/<int:id_room>/", views.GetUserByIdRoom().as_view()),
    path("api/users/rooms/<int:id_room>", views.GetUsersByIdRoom().as_view()),
    path("api/users/send/", views.MoneyTransfer().as_view())

]