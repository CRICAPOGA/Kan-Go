from django.urls import path
from . import views

urlpatterns = [
    path('', views.pomodoro, name='pomodoro'),
    path('añadir/<int:id>', views.añadir, name="añadir"),
    path('eliminar/<str:id>/', views.eliminar, name="eliminar"),
]