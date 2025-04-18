from django.shortcuts import render, get_object_or_404
from Proyectos.models import Proyecto
from .models import Tarea
from django.http import JsonResponse
import json

def tablero_kanban(request, proyecto_id):
    # Obtener proyecto y tareas asociadas
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    tareas = Tarea.objects.filter(proyecto_id=proyecto)
    # Diccionario para pasar datos a la plantilla
    contexto = {
        'proyecto': proyecto,
        'tareas_por_hacer': tareas.filter(estado=0),
        'tareas_en_progreso': tareas.filter(estado=1),
        'tareas_hechas': tareas.filter(estado=2),
    }
    return render(request, 'kanban.html', contexto)

def actualizar_estado_tarea(request):
    if request.method == "POST":
        # Obtener datos
        data = json.loads(request.body)
        # Buscar tarea en la BD
        tarea = get_object_or_404(Tarea, pk=data["tarea_id"])
        # Actualizar estado
        tarea.estado = data["estado"]
        tarea.save()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Método no permitido"}, status=405)
