from django.urls import path
from . import views

app_name = 'etiquetas'

urlpatterns = [
    path('crear/', views.crear_etiqueta, name='crear_etiqueta'),
    path('listar/', views.listar_etiquetas, name='listar_etiquetas'),
    path('editar/<int:etiqueta_id>/', views.editar_etiqueta, name='editar_etiqueta'),
]