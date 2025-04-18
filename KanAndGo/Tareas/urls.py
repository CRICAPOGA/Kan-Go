from django.urls import path
from . import views
app_name = 'tareas'

urlpatterns = [
    path('kanban/<int:proyecto_id>/', views.tablero_kanban, name='kanban'),
    path('actualizar_estado/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('crear/<int:proyecto_id>/', views.crear_tarea, name='crear_tarea'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea')
]