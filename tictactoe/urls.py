from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("game/status",views.game_status,name="game_status"),
    path("game/move",views.next_move,name="next_move"),
]