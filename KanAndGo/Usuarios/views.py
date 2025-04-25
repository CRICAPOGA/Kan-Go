from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Usuario, Rol
from .forms import UsuarioForm
from django.contrib import messages

@staff_member_required(login_url='/')
@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    roles = Rol.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'roles': roles})

@staff_member_required(login_url='/')
@login_required
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

@staff_member_required(login_url='/')
@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return redirect('lista_usuarios')

@staff_member_required(login_url='/')
@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'usuarios.html', {'form': form, 'usuario': usuario})

@staff_member_required(login_url='/')
@login_required
def crear_rol(request):
    roles = Rol.objects.all()
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        if nuevo_rol:
            Rol.objects.create(rol=nuevo_rol)
            return redirect('lista_usuarios')  # Nombre de la url que renderiza usuarios.html

    return render(request, 'usuarios.html', {'roles': roles, 'usuarios': usuarios})

@login_required
@staff_member_required(login_url='/')
def editar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('rol')
        if nuevo_nombre:
            rol.rol = nuevo_nombre
            rol.save()
            messages.success(request, 'Rol actualizado correctamente.')
        return redirect('lista_usuarios')
    return redirect('lista_usuarios')

@staff_member_required(login_url='/')
@login_required
def eliminar_rol(request, rol_id):
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente.')
    return redirect('lista_usuarios')


