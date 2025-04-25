from django.shortcuts import render, redirect, get_object_or_404
from .models import Temporizadores
from .forms import PomodoroForm
from django.contrib.auth.decorators import login_required

@login_required
def pomodoro(request):
    temporizadores = Temporizadores.objects.all().order_by('prioridad')
    formulario = PomodoroForm(request.POST or None, usuario=request.user)  # Manejar POST o inicialización vacía

    if request.method == 'POST':  # Verificar si la solicitud es POST
        if formulario.is_valid():  # Validar el formulario
            formulario.save()  # Guardar el formulario
            return redirect('pomodoro')  # Redirigir para evitar reenvío del formulario

    return render(request, 'pomodoro.html', {
        'formulario': formulario,
        'temporizadores': temporizadores,
    })

@login_required
def eliminar_temporizador(request, id):
    temporizador = get_object_or_404(Temporizadores, id=id, usuario_id=request.user)
    if request.method == 'POST':
        temporizador.delete()
        return redirect('pomodoro')