from django.urls import path
from . import views

app_name = 'proyectos'

urlpatterns = [
    path('', views.proyectos, name='proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
]