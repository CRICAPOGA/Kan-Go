from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EtiquetaForm
from .models import Etiqueta

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            etiqueta = form.save(commit=False)
            etiqueta.usuario_id = request.user  # Asignar el usuario actual
            etiqueta.save()
            return redirect('home')  # Cambiar por la vista deseada
    else:
        form = EtiquetaForm()
    return render(request, 'crear_etiqueta.html', {'form': form})
