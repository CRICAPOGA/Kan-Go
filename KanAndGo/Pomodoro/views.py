from django.shortcuts import render, redirect, get_object_or_404
from .models import Temporizadores
from .forms import PomodoroForm
from django.contrib.auth.decorators import login_required

@login_required
def pomodoro(request):
    titulo_tarea = request.GET.get('tarea', '')  # Obtener el título de la tarea desde los parámetros
    temporizadores = Temporizadores.objects.filter(usuario_id=request.user).order_by('prioridad')
    formulario = PomodoroForm(request.POST or None, usuario=request.user)

    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            return redirect('pomodoro')

    return render(request, 'pomodoro.html', {
        'formulario': formulario,
        'temporizadores': temporizadores,
        'titulo_tarea': titulo_tarea,  # Pasar el título de la tarea al contexto
    })

@login_required
def eliminar_temporizador(request, id):
    temporizador = get_object_or_404(Temporizadores, id=id, usuario_id=request.user)
    if request.method == 'POST':
        temporizador.delete()
        return redirect('pomodoro')