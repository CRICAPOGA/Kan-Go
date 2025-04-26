from django.shortcuts import render, redirect, get_object_or_404
from .models import Temporizadores
from .forms import PomodoroForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def pomodoro(request):
    titulo_tarea = request.GET.get('tarea', '')  # Obtener el título de la tarea desde los parámetros
    temporizadores = Temporizadores.objects.filter(usuario_id=request.user).order_by('prioridad')
    formulario = PomodoroForm(request.POST or None, usuario=request.user)

    # Serializar los temporizadores para enviarlos al frontend
    temporizadores_data = [
        {
            'id': t.id,
            'titulo': t.titulo,
            'horas': t.horas,
            'minutos': t.minutos,
            'segundos': t.segundos,
            'prioridad': t.prioridad,
        }
        for t in temporizadores
    ]

    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            return redirect('pomodoro')

    return render(request, 'pomodoro.html', {
        'formulario': formulario,
        'temporizadores': temporizadores,
        'temporizadores_json': temporizadores_data,  # Pasar los datos serializados
        'titulo_tarea': titulo_tarea,  # Pasar el título de la tarea al contexto
    })

@login_required
def eliminar_temporizador(request, id):
    temporizador = get_object_or_404(Temporizadores, id=id, usuario_id=request.user)
    if request.method == 'POST':
        temporizador.delete()
        return redirect('pomodoro')