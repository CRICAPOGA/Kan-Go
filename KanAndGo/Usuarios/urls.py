from django.urls import path
from . import views

urlpatterns = [
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
]