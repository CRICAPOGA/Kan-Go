from django.urls import path
from . import views

urlpatterns = [
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),
    path('roles/editar/<int:rol_id>/', views.editar_rol, name='editar_rol'),
    path('roles/eliminar/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol')
]