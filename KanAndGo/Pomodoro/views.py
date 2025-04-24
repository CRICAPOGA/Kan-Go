from django.shortcuts import render, redirect
from .models import Temporizadores
from .forms import PomodoroForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def pomodoro(request):
  temporizadores = Temporizadores.objects.all().order_by('prioridad')
  formulario = PomodoroForm()
  
  if len(temporizadores) == 0:
      return render(request, 'pomodoro.html', {
          'formulario': formulario,
          'editable': False,
          'temporizadores': None,
      })
  
  return render(request, 'pomodoro.html', {
      'form': formulario,
      'editable': False,
      'temporizadores': temporizadores,
  })