from django.urls import path
from . import views

urlpatterns = [
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
]