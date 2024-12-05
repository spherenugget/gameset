from django.urls import path
from gamesetwebapp.views.indexview import GameDetailView, IndexView, TrendView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('', TrendView.as_view(), name='trend'),
    path('', GameDetailView.as_view(), name='game-detail'),
]
