from django.shortcuts import render, redirect
from .models import Usuario, Rol
from .forms import UsuarioForm

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    roles = Rol.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'roles': roles})

def crear_usuario(request):
    roles = Rol.objects.all()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')  # Redirige a la lista de usuarios
    else:
        form = UsuarioForm()

    return render(request, 'usuarios.html', {'form': form, 'roles': roles})