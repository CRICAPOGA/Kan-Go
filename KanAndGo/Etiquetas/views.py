from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EtiquetaForm
from .models import Etiqueta

@login_required
def listar_etiquetas(request):
    etiquetas = Etiqueta.objects.all()  # Obtiene todas las etiquetas
    print(etiquetas)
    return render(request, 'listar.html', {'etiquetas': etiquetas})

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            etiqueta = form.save(commit=False)
            etiqueta.usuario_id = request.user  # Asignar el usuario actual
            etiqueta.save()
            return redirect('etiquetas:listar_etiquetas')  # Cambiar por la vista deseada
    else:
        form = EtiquetaForm()
    return render(request, 'listar.html', {'form': form})

@login_required
def editar_etiqueta(request, etiqueta_id):
    etiqueta = Etiqueta.objects.get(pk=etiqueta_id)
    
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            return redirect('etiquetas:listar_etiquetas')

def eliminar_etiqueta(request, etiqueta_id):
    etiqueta = get_object_or_404(Etiqueta, pk=etiqueta_id)
    if request.method == 'POST':
        etiqueta.delete()
        return redirect('etiquetas:listar_etiquetas')