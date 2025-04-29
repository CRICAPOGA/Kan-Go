from django.urls import path
from . import views

app_name = 'etiquetas'

urlpatterns = [
    path('listar/', views.listar_etiquetas, name='listar_etiquetas'),
    path('crear/', views.crear_etiqueta, name='crear_etiqueta'), 
    path('editar/<int:etiqueta_id>/', views.editar_etiqueta, name='editar_etiqueta'),
    path('eliminar/<int:etiqueta_id>/', views.eliminar_etiqueta, name='eliminar_etiqueta')
]