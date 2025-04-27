from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EtiquetaForm
from .models import Etiqueta

@login_required
def listar_etiquetas(request):
    etiquetas = Etiqueta.objects.filter(usuario_id=request.user)
    return render(request, 'etiquetas/listar_etiquetas.html', {'etiquetas': etiquetas})

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            # Guardar la etiqueta pero sin confirmar el commit aún
            etiqueta = form.save(commit=False)
            etiqueta.usuario_id = request.user  # Asignar usuario actual
            etiqueta.save()
            return redirect(request.META.get('HTTP_REFERER', 'kanban.html'))  # Regresa a la página anterior
    else:
        form = EtiquetaForm()
    
    return render(request, 'crear_etiqueta.html', {'form': form})

@login_required
def editar_etiqueta(request, etiqueta_id):
    etiqueta = get_object_or_404(Etiqueta, pk=etiqueta_id)
    
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            return redirect('etiquetas:listar_etiquetas')  # O la redirección que prefieras
    else:
        form = EtiquetaForm(instance=etiqueta)
    
    return render(request, 'editar_etiqueta.html', {'form': form, 'etiqueta': etiqueta})


