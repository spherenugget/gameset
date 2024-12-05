from django.urls import path
from gamesetwebapp.views.indexview import IndexView
from gamesetwebapp.views.gameview import GameDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game/<int:game_name>/', GameDetailView.as_view(), name='game-detail'),
]
