import pytest
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from Usuarios.models import Usuario, Rol

@pytest.mark.django_db
def test_login_auth_credenciales_validas(client, django_user_model):
    # Crear un usuario de prueba
    usuario = django_user_model.objects.create_user(username='usuarioprueba', password='contraseñaprueba')
    
    # Enviar datos válidos al endpoint de inicio de sesión
    respuesta = client.post(reverse('login_auth'), {'username': 'usuarioprueba', 'password': 'contraseñaprueba'})
    
    # Verificar que el usuario fue autenticado correctamente
    assert respuesta.status_code == 200
    assert respuesta.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_login_auth_credenciales_invalidas(client):
    # Enviar datos inválidos al endpoint de inicio de sesión
    respuesta = client.post(reverse('login_auth'), {'username': 'usuariomalo', 'password': 'contraseñamala'})
    
    # Verificar que el usuario no fue autenticado
    assert respuesta.status_code == 200
    assert not respuesta.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_logout_view(client, django_user_model):
    # Crear un usuario de prueba y autenticarlo
    usuario = django_user_model.objects.create_user(username='usuarioprueba', password='contraseñaprueba')
    client.login(username='usuarioprueba', password='contraseñaprueba')
    
    # Llamar al endpoint de cierre de sesión
    respuesta = client.get(reverse('logout'))
    
    # Verificar que el usuario fue desconectado
    assert respuesta.status_code == 200
    assert isinstance(respuesta.wsgi_request.user, AnonymousUser)

@pytest.mark.django_db
def test_registro_auth_datos_validos(client):
    # Crear un rol de prueba
    rol = Rol.objects.create(rol='Rol de Prueba')
    
    # Enviar datos válidos al endpoint de registro
    respuesta = client.post(reverse('register'), {
        'nombre': 'Prueba',
        'apellido': 'Usuario',
        'username': 'usuarioprueba',
        'correo': 'usuarioprueba@example.com',
        'password': 'contraseñaprueba',
    })
    
    # Verificar que el usuario fue registrado correctamente
    assert respuesta.status_code == 302  # Redirección después del registro
    assert Usuario.objects.filter(username='usuarioprueba').exists()

@pytest.mark.django_db
def test_registro_auth_nombre_usuario_existente(client, django_user_model):
    # Crear un usuario de prueba
    django_user_model.objects.create_user(username='usuarioprueba', password='contraseñaprueba')
    
    # Enviar datos con un nombre de usuario existente
    respuesta = client.post(reverse('register'), {
        'nombre': 'Prueba',
        'apellido': 'Usuario',
        'username': 'usuarioprueba',
        'correo': 'usuarioprueba2@example.com',
        'password': 'contraseñaprueba',
    })
    
    # Verificar que el registro falló debido a un nombre de usuario existente
    assert respuesta.status_code == 302  # Redirección después del error
    assert Usuario.objects.filter(username='usuarioprueba').count() == 1

@pytest.mark.django_db
def test_vista_acceso(client):
    # Verificar que la vista de acceso se carga correctamente
    respuesta = client.get(reverse('acceso'))
    assert respuesta.status_code == 200
    assert 'acceso.html' in [t.name for t in respuesta.templates]