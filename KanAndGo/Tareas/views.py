from django.shortcuts import render, get_object_or_404, redirect
from Proyectos.models import Proyecto
from Etiquetas.models import Etiqueta, DetalleEtiqueta
from .models import Tarea
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.db import models
from .forms import TareaForm
from calendar import monthrange
from datetime import date
from django.contrib.auth.decorators import login_required

@login_required
def calendario(request):
    proyectos = Proyecto.objects.filter(fecha_finalizacion__isnull=False)
    return render(request, 'calendario.html', {'proyectos': proyectos})

@login_required
def calendario(request):
    hoy = date.today()
    mes = int(request.GET.get('mes', hoy.month))
    anio = int(request.GET.get('anio', hoy.year))
    
    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, monthrange(anio, mes)[1])

    tareas = Tarea.objects.filter(fecha_vencimiento__range=(primer_dia, ultimo_dia))

    tareas_dict = {}
    for tarea in tareas:
        fecha_str = tarea.fecha_vencimiento.strftime('%Y-%m-%d')
        if fecha_str not in tareas_dict:
            tareas_dict[fecha_str] = []
        tareas_dict[fecha_str].append({
            'id': tarea.tarea_id,
            'titulo': tarea.titulo,
            'proyecto': tarea.proyecto_id.nombre_proyecto,
        })

    contexto = {
        'mes': mes,
        'anio': anio,
        'tareas_json': json.dumps(tareas_dict or {})
    }

    return render(request, 'calendario.html', contexto)

@login_required
def tablero_kanban(request, proyecto_id):
    # Obtener proyecto y tareas asociadas
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    tareas = Tarea.objects.filter(proyecto_id=proyecto)
    # Orden:
    # 1. urgente = True e importante = True → prioridad 0
    # 2. urgente = True e importante = False → prioridad 1
    # 3. urgente = False e importante = True → prioridad 2
    # 4. urgente = False e importante = False → prioridad 3
    def orden_prioridad(qs):
        return qs.annotate(
            prioridad=models.Case(
                models.When(es_urgente=True, es_importante=True, then=models.Value(0)),
                models.When(es_urgente=True, es_importante=False, then=models.Value(1)),
                models.When(es_urgente=False, es_importante=True, then=models.Value(2)),
                default=models.Value(3),
                output_field=models.IntegerField()
            )
        ).order_by('prioridad')
    # Diccionario para pasar datos a la plantilla
    contexto = {
        'proyecto': proyecto,
        'tareas_por_hacer': orden_prioridad(tareas.filter(estado=0)),
        'tareas_en_progreso': orden_prioridad(tareas.filter(estado=1)),
        'tareas_hechas': orden_prioridad(tareas.filter(estado=2)),
        'etiquetas': Etiqueta.objects.filter(usuario_id=request.user),
    }
    return render(request, 'kanban.html', contexto)

@login_required
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

@login_required
def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            nueva_tarea = form.save(commit=False)
            nueva_tarea.proyecto_id = proyecto  # Asociar la tarea al proyecto
            nueva_tarea.save()
            return redirect('tareas:kanban', proyecto_id=proyecto_id)
        else:
            form = TareaForm()
    return render(request, 'kanban.html', {'form': form})

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas:kanban', proyecto_id=tarea.proyecto_id.proyecto_id)
    return redirect('tareas:kanban', proyecto_id=tarea.proyecto_id.proyecto_id)

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas:kanban', proyecto_id=tarea.proyecto_id.proyecto_id)
    else:
        form = TareaForm(instance=tarea)
    
    return render(request, 'editar_tarea.html', {'form': form, 'tarea': tarea})