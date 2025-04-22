from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_etiqueta, name='crear_etiqueta'),
]