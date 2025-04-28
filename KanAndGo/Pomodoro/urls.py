from django.urls import path
from . import views

urlpatterns = [
    path('', views.pomodoro, name='pomodoro'),
    path('eliminar/<int:id>/', views.eliminar_temporizador, name='eliminar_temporizador'),
    path('marcar_como_finalizada/', views.marcar_como_finalizada, name='marcar_como_finalizada'),
]