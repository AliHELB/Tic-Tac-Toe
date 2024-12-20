from django.urls import path
from .views import (
    GameListView,
    GameCreateView,
    GameUpdateView,
    GameDeleteView,
    GameDetailView,
    GamePlayView,
    JoinPrivateGameView,
    make_move,
    get_data,
    join_public_game,
    surrender,
    set_winner,
    statistics,
)
from . import views

urlpatterns = [
    path('', GameListView.as_view(), name='morpion-home'),  #localhost:8000/morpion/
    path('game/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('game/new/', GameCreateView.as_view(), name='game-create'),
    path('game/<int:pk>/update/', GameUpdateView.as_view(), name='game-update'),
    path('game/<int:pk>/delete/', GameDeleteView.as_view(), name='game-delete'),
    path('game/<int:pk>/play/', GamePlayView.as_view(), name='game-play'),
    path('game/<int:game_id>/join/', JoinPrivateGameView.as_view(), name='join-private-game'),
    path('game/<int:game_id>/joinpublic/', join_public_game, name='join-public-game'),
    path('statistics/', statistics, name='statistics'),
    path('game/<int:pk>/make-move/', make_move, name='make-move'),
    path('game/<int:game_id>/get-data/', get_data, name='get-data'),
    path('game/<int:pk>/surrender/', surrender, name='surrender'),
    path('game/<int:pk>/set-winner/', set_winner, name='set-winner'),
]