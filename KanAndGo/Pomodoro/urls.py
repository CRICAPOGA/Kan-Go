from django.urls import path
from . import views

urlpatterns = [
    path('', views.pomodoro, name='pomodoro'),
    path('eliminar/<int:id>/', views.eliminar_temporizador, name='eliminar_temporizador'),
]