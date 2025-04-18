from django.shortcuts import render, redirect
from .models import Proyecto
from .forms import ProyectoForm

######################### CRUD PROYECTOS #########################
def proyectos(request):
    proyectos = Proyecto.objects.filter(usuario_id=request.user)
    return render(request, 'proyectos.html', {'proyectos': proyectos})

def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            nuevo_proyecto = form.save(commit=False)
            nuevo_proyecto.usuario_id = request.user
            nuevo_proyecto.estado = True
            nuevo_proyecto.save()
            return redirect('proyectos:proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})
