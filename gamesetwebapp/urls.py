from django.urls import path
from gamesetwebapp.views.indexview import IndexView 
from gamesetwebapp.views.gameview import GameDetailView, TrendView

# gamesetwebapp/urls.py

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game/<int:game_id>/', GameDetailView.as_view(), name='game_detail'), 
    path('trend/', TrendView.as_view(), name='trend'),
]

