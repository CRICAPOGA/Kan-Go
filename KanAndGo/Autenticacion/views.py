from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Usuarios.models import Usuario, Rol

def login_auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['password']
        user = authenticate(request, username=username, password=contraseña)
        if user is not None:
            login(request, user)  # Inicia la sesión del usuario
            return render(request, 'home.html')
        else:
            messages.error(request,'Credenciales incorrectas')
            return render(request, 'acceso.html')
    return render(request, 'acceso.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'acceso.html')

def register_auth(request):
    roles = Rol.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        username = request.POST['username']
        correo = request.POST['correo']
        password = request.POST['password']
        rol_id = 1

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('acceso')

        usuario = Usuario.objects.create_user(
            username=username,
            correo=correo,
            password=password
        )
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.rol_id = Rol.objects.get(rol_id=rol_id) if rol_id else None
        usuario.save()
        
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('acceso')
    
    return render(request, 'acceso.html', {'roles': roles})

def acceso(request):
    return render(request, 'acceso.html')

from django.core.mail import send_mail
from django.http import HttpResponse

def prueba_correo(request):
    try:
        send_mail(
            subject='Prueba de correo',
            message='Este es un correo de prueba enviado desde Django.',
            from_email='abff679d82757c@mailtrap.io',  # Usa el correo configurado en Mailtrap
            recipient_list=['camilochoposada2@example.com'],  # Cambia esto por un correo válido
            fail_silently=False,
        )
        return HttpResponse("Correo enviado exitosamente.")
    except Exception as e:
        return HttpResponse(f"Error al enviar el correo: {e}")
