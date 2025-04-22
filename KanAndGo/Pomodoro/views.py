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

@login_required
def añadir(request,id):
    editable = True
    if request.method == "POST":
        editable = False
        formulario = PomodoroForm(request.POST)
        if formulario.is_valid():
            form_instance = formulario.save(commit=False)
            form_instance.uuid = id
            form_instance.save()
            return redirect("pomodoro")
    else:
        formulario = PomodoroForm()
        temporizadores = Temporizadores.objects.all()
        return render(request, 'pomodoro.html', {
            'formulario': formulario,
            "editable": editable,
            'temporizadores': temporizadores
        })

@login_required
def eliminar(request, id):
    temporizadores = Temporizadores.objects.get(id=id)
    temporizadores.delete()
    print("Successfully Deleted {{id}}")
    temporizadores = Temporizadores.objects.all()
    formulario = PomodoroForm()
    if len(temporizadores) == 0:
        return render(request, 'pomodoro.html', {
            'formulario': formulario,
            "editable": False,
            'temporizadores': None
        })
    return render(request, 'pomodoro.html', {
        'formulario': formulario,
        "editable": False,
        'temporizadores': temporizadores
    })