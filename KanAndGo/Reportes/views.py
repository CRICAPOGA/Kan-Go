from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Proyectos.models import Proyecto
from Pomodoro.models import Sesiones
from Tareas.models import Tarea
from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay
from django.utils.timezone import now
import json
from django.core.serializers.json import DjangoJSONEncoder
import pytz
import locale


@login_required
def reportes(request):
    proyectos = get_proyectos(request.user)

    # Filtros de fecha
    rango_fecha = calcular_rango_fecha(request.GET)

    # Filtrar proyectos si corresponde
    if rango_fecha:
        proyectos = proyectos.filter(estado=True)  # Filtrar por estado activo

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

    # Total de sesiones SOLO del proyecto seleccionado
    total_sesiones = 0
    sesiones = Sesiones.objects.none() 
    if proyecto_seleccionado:
        sesiones = Sesiones.objects.filter(
            tarea_id__proyecto_id=proyecto_seleccionado
    )
    total_sesiones = sesiones.aggregate(total_sesiones=Sum('sesiones'))['total_sesiones'] or 0
    
    # Sesiones por Tarea
    sesiones_por_tarea = sesiones.values(
        'tarea_id__titulo',
    ).annotate(
        total_sesiones=Sum('sesiones')
    ).order_by('-total_sesiones')

    # Métricas de Sesiones Pomodoro
    metricas_sesiones = calcular_metricas_sesiones(request.user)

    # Resumen General de Sesiones Pomodoro
    resumen_general_sesiones = calcular_metricas_sesiones(request.user, rango_fecha)
    
    # 1. Reporte general de sesiones por todos los proyectos (NO filtrar)
    sesiones_por_proyecto = Sesiones.objects.filter(
        tarea_id__proyecto_id__usuario_id=request.user.usuario_id
    )

    if rango_fecha:
        sesiones_por_proyecto = sesiones_por_proyecto.filter(fecha__range=rango_fecha)

    sesiones_por_proyecto = sesiones_por_proyecto.values(
        'tarea_id__proyecto_id__nombre_proyecto'
    ).annotate(
        total_sesiones=Sum('sesiones')
    ).order_by('-total_sesiones')

    # 2. Resumen de sesiones pomodoro del proyecto seleccionado (SÍ filtrar)
    sesiones_resumen_proyecto = None
    if proyecto_seleccionado:
        sesiones_resumen_proyecto = Sesiones.objects.filter(
            tarea_id__proyecto_id=proyecto_seleccionado
        ).values(
            'tarea_id__titulo',
        ).annotate(
            total_sesiones=Sum('sesiones')
        ).order_by('-total_sesiones')
    
    # Calcular tiempo dedicado por proyecto (llamando a la función calcular_tiempo_por_proyecto)
    tiempo_por_proyecto = calcular_tiempo_por_proyecto(sesiones_por_proyecto) if sesiones_por_proyecto else []

    print(resumen_proyectos)  # Para asegurarte de que los datos se están generando correctamente


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
        'total_sesiones':total_sesiones, # Total sesiones del proyecto seleccionado
        'sesiones_por_tarea': sesiones_resumen_proyecto,  # Solo del proyecto seleccionado
        'sesiones_por_tarea_json': json.dumps(list(sesiones_resumen_proyecto) if sesiones_resumen_proyecto else [], cls=DjangoJSONEncoder),
        'no_hay_sesiones': not sesiones_resumen_proyecto.exists() if sesiones_resumen_proyecto else True,
        'metricas_sesiones': metricas_sesiones,
        'sesiones_por_proyecto': sesiones_por_proyecto,  # Para el reporte general
        'tiempo_por_proyecto': tiempo_por_proyecto,
        'resumen_general_sesiones': resumen_general_sesiones,
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
            'proyecto_id': proyecto.proyecto_id,
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

def calcular_metricas_sesiones(usuario, rango_fecha=None):
    # Establecer el locale a español de Colombia para nombres de días
    try:
        locale.setlocale(locale.LC_TIME, 'es_CO.UTF-8')  # Para sistemas Linux
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Alternativa si 'es_CO' no existe
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')  # Dejarlo en el sistema por defecto si falla

    # Usar la zona horaria de Colombia
    zona_colombia = pytz.timezone('America/Bogota')

    # Traer las sesiones ajustadas a la zona horaria de Colombia
    sesiones = Sesiones.objects.filter(tarea_id__proyecto_id__usuario_id=usuario)
    if rango_fecha:
        sesiones = sesiones.filter(fecha__range=rango_fecha)

    total_sesiones = sesiones.aggregate(total=Sum('sesiones'))['total'] or 0

    # Total de horas y minutos
    total_minutos_trabajados = total_sesiones * 25
    horas_trabajadas = total_minutos_trabajados // 60
    minutos_trabajados = total_minutos_trabajados % 60

    # Mostrar el resultado en formato "hora:minuto"
    total_horas_trabajadas = f"{int(horas_trabajadas)}:{int(minutos_trabajados):02d}"

    # Calcular promedio de sesiones por día
    dias_unicos = sesiones.values('fecha').distinct().count()
    promedio_sesiones_dia = round(total_sesiones / dias_unicos, 2) if dias_unicos > 0 else 0

    # Calcular el día más productivo
    sesiones_por_dia = sesiones.annotate(dia_semana=ExtractWeekDay('fecha')) \
                                .values('dia_semana') \
                                .annotate(total=Sum('sesiones')) \
                                .order_by('-total')

    if sesiones_por_dia:
        dia_mas_productivo = sesiones_por_dia[0]
        # Convertir número de día a nombre en español
        dia_numero = (dia_mas_productivo['dia_semana'] - 1) % 7  # Ajuste de índice
        nombre_dia = (now().astimezone(zona_colombia) + timedelta(days=(dia_numero - now().weekday()) % 7)).strftime('%A').capitalize()
        sesiones_maximas = dia_mas_productivo['total']
    else:
        nombre_dia = "Sin datos"
        sesiones_maximas = 0

    metricas = {
        'total_sesiones': total_sesiones,
        'total_horas_trabajadas': total_horas_trabajadas,
        'promedio_sesiones_dia': promedio_sesiones_dia,
        'dia_mas_productivo': nombre_dia,
        'sesiones_en_dia_mas_productivo': sesiones_maximas,
    }

    return metricas

def calcular_tiempo_por_proyecto(sesiones_por_proyecto):
    tiempo_por_proyecto = []
    for item in sesiones_por_proyecto:
        nombre_proyecto = item['tarea_id__proyecto_id__nombre_proyecto']
        total_sesiones = item['total_sesiones'] or 0
        total_minutos = total_sesiones * 25  # Cada sesión son 25 min
        horas = total_minutos // 60
        minutos = total_minutos % 60
        tiempo_por_proyecto.append({
            'proyecto': nombre_proyecto,
            'sesiones': total_sesiones,
            'tiempo': f"{horas}h {minutos}m",
        })
    return tiempo_por_proyecto
