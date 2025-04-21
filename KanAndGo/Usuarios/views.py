from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Usuario, Rol
from .forms import UsuarioForm

#@staff_member_required(login_url='/')
#@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    roles = Rol.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'roles': roles})

#@staff_member_required(login_url='/')
#@login_required
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

#@staff_member_required(login_url='/')
#@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return redirect('lista_usuarios')
