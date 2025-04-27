from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Proyectos.models import Proyecto
from Tareas.models import Tarea
from django.db.models import Count, Q, Avg

@login_required
def reportes(request):
    proyectos = get_proyectos(request.user)

    # Filtros de fecha
    rango_fecha = calcular_rango_fecha(request.GET)

    # Filtrar proyectos si corresponde
    if rango_fecha:
        proyectos = proyectos.filter(fecha_creacion__range=rango_fecha)  # Asegúrate de que `fecha_inicio` esté en tu modelo de Proyecto

    proyecto_id = request.GET.get('proyecto_id')
    proyecto_seleccionado, tareas = get_proyecto_seleccionado(proyecto_id, request.user)

    # Asegúrate de que si se ha seleccionado un proyecto, no se filtre por fechas en tareas
    if proyecto_seleccionado:
        tareas = Tarea.objects.filter(proyecto_id=proyecto_seleccionado)
    elif rango_fecha and tareas.exists():
        tareas = tareas.filter(fecha_vencimiento__range=rango_fecha)

    # Calcular datos por proyecto
    resumen_proyectos = calcular_resumen_proyectos(proyectos)

    # Obtener el máximo número de tareas pendientes
    max_pendientes = max([proyecto['pendientes'] for proyecto in resumen_proyectos], default=0)

    # Filtrar todos los proyectos con número máximo de tareas pendientes
    proyectos_mas_pendientes = [proyecto for proyecto in resumen_proyectos if proyecto['pendientes'] == max_pendientes and proyecto['pendientes'] > 0]

    # Métricas Generales
    total_proyectos, activos, completados = calcular_metricas_generales(proyectos)
    avance_promedio = calcular_avance_promedio(resumen_proyectos)

    # Calcular datos de tareas solo si se seleccionó un proyecto
    total_tareas, tareas_completadas, tareas_en_progreso, tareas_pendientes, tareas_vencidas, avance_general = calcular_tareas(tareas)

    contexto = {
        'proyectos': proyectos,
        'proyecto_id': proyecto_id,
        'proyecto_seleccionado': proyecto_seleccionado,
        'rango_fecha': rango_fecha,
        'total_tareas': total_tareas,
        'tareas_completadas': tareas_completadas,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_pendientes': tareas_pendientes,
        'tareas_vencidas': tareas_vencidas,
        'avance_general': avance_general,
        'resumen_proyectos': resumen_proyectos,
        'total_proyectos': total_proyectos,
        'activos': activos,
        'completados': completados,
        'avance_promedio': avance_promedio,
        'proyectos_mas_pendientes': proyectos_mas_pendientes,
    }

    return render(request, 'reportes.html', contexto)

# Recuperar todos los proyectos del usuario
def get_proyectos(user):
    return Proyecto.objects.filter(usuario_id=user)

# Recuperar proyecto seleccionado y sus tareas
def get_proyecto_seleccionado(proyecto_id, user):
    proyecto_seleccionado = None
    tareas = Tarea.objects.none()
    if proyecto_id:
        proyecto_seleccionado = Proyecto.objects.filter(proyecto_id=proyecto_id, usuario_id=user).first()
        if proyecto_seleccionado:
            tareas = Tarea.objects.filter(proyecto_id=proyecto_seleccionado)
    return proyecto_seleccionado, tareas

# Calcular rango de fechas según el filtro seleccionado
def calcular_rango_fecha(params):
    fecha_filtro = params.get('fecha_filtro')
    fecha_inicio = params.get('fecha_inicio')
    fecha_fin = params.get('fecha_fin')

    rango_fecha = None
    if fecha_filtro == 'semana':
        hoy = now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        rango_fecha = (inicio_semana, fin_semana)

    elif fecha_filtro == 'mes':
        hoy = now().date()
        inicio_mes = hoy.replace(day=1)
        rango_fecha = (inicio_mes, hoy)

    elif fecha_filtro == 'personalizado' and fecha_inicio and fecha_fin:
        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            rango_fecha = (inicio, fin)
        except ValueError:
            rango_fecha = None
    return rango_fecha

# Resumen de tareas por cada proyecto (tabla)
def calcular_resumen_proyectos(proyectos):
    resumen_proyectos = []
    for proyecto in proyectos:
        tareas_proyecto = Tarea.objects.filter(proyecto_id=proyecto)
        total = tareas_proyecto.count()
        completadas = tareas_proyecto.filter(estado=2).count()
        en_proceso = tareas_proyecto.filter(estado=1).count()
        pendientes = tareas_proyecto.filter(estado=0).count()
        avance = (completadas / total * 100) if total > 0 else 0
        resumen_proyectos.append({
            'nombre': proyecto.nombre_proyecto,
            'estado': proyecto.estado,
            'avance': round(avance, 2),
            'pendientes': pendientes,
            'en_proceso': en_proceso,
            'completadas': completadas,
            'total_tareas': total,
        })
    return resumen_proyectos

# Información general de los proyectos
def calcular_metricas_generales(proyectos):
    total_proyectos = proyectos.count()
    activos = proyectos.filter(estado=True).count()
    completados = proyectos.filter(estado=False).count()
    return total_proyectos, activos, completados

# Calcular el avance promedio de los proyectos activos
def calcular_avance_promedio(resumen_proyectos):
    activos_lista = [p for p in resumen_proyectos if p['estado'] == True]
    avance_promedio = round(sum(p['avance'] for p in activos_lista) / len(activos_lista), 2) if activos_lista else 0
    return avance_promedio

# Obtener detalles de las tareas (resumen general del proyecto)
def calcular_tareas(tareas):
    total_tareas = tareas.count()
    tareas_completadas = tareas.filter(estado=2).count()
    tareas_en_progreso = tareas.filter(estado=1).count()
    tareas_pendientes = tareas.filter(estado=0).count()
    tareas_vencidas = tareas.filter(fecha_vencimiento__lt=now().date()).count()

    avance_general = 0
    if total_tareas > 0:
        avance_general = (tareas_completadas / total_tareas) * 100

    return total_tareas, tareas_completadas, tareas_en_progreso, tareas_pendientes, tareas_vencidas, avance_general