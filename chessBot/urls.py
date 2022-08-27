from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chess/nextMoveSunFish/', views.nextMoveSunFish , name='nextMoveSunFish'),
]