from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Proyecto
from .forms import ProyectoForm

######################### CRUD PROYECTOS #########################
@login_required
def proyectos(request):
    proyectos = Proyecto.objects.filter(usuario_id=request.user)
    return render(request, 'proyectos.html', {'proyectos': proyectos})

@login_required
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
    return render(request, 'proyectos.html', {'form': form})

@login_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id, usuario_id=request.user)
    # Si la solicitud es POST guardar cambios
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('proyectos:proyectos')
    else:
        # Crear form cargando los datos actuales desde la BD
        form = ProyectoForm(instance=proyecto)
    # Verificar por XMLHttpRequest si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'editar_proyecto.html', {'form': form, 'proyecto': proyecto})

    return render(request, 'editar_proyecto.html', {'form': form, 'proyecto': proyecto})

@login_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id, usuario_id=request.user)

    if request.method == 'POST':
        proyecto.delete()
        return redirect('proyectos:proyectos')

    return redirect('proyectos:proyectos')
