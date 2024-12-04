from django.urls import path
from gamesetwebapp.views.indexview import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='trend')
]
