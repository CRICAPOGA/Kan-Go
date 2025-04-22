import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from Usuarios.models import Usuario, Rol

@pytest.fixture
def cliente_admin(client):
    # Crear un usuario administrador para las pruebas usando el modelo personalizado Usuario
    usuario_admin = Usuario.objects.create_user(
        username="admin",
        password="admin123",
        is_staff=True,
        is_superuser=True,  # Asegúrate de que sea superusuario si es necesario
        correo="admin@ejemplo.com",
        nombre="Admin",
        apellido="Usuario"
    )
    client.login(username="admin", password="admin123")
    return client

@pytest.mark.django_db
def test_vista_lista_usuarios(cliente_admin):
    # Crear datos de prueba
    rol = Rol.objects.create(rol="Admin")
    Usuario.objects.create(username="usuario1", correo="usuario1@ejemplo.com", rol_id=rol)
    Usuario.objects.create(username="usuario2", correo="usuario2@ejemplo.com", rol_id=rol)

    # Acceder a la vista
    url = reverse('lista_usuarios')
    respuesta = cliente_admin.get(url)

    # Aserciones
    assert respuesta.status_code == 200
    assert "usuario1" in respuesta.content.decode()
    assert "usuario2" in respuesta.content.decode()

@pytest.mark.django_db
def test_vista_crear_usuario(cliente_admin):
    rol = Rol.objects.create(rol="Admin")
    url = reverse('crear_usuario')
    datos = {
        "username": "nuevousuario",
        "correo": "nuevousuario@ejemplo.com",
        "nombre": "Nuevo",
        "apellido": "Usuario",
        "rol_id": rol.rol_id,
        "password": "contraseña123"
    }

    respuesta = cliente_admin.post(url, datos)

    # Aserciones
    assert respuesta.status_code == 302  # Redirección después de la creación
    assert Usuario.objects.filter(username="nuevousuario").exists()

@pytest.mark.django_db
def test_vista_eliminar_usuario(cliente_admin):
    rol = Rol.objects.create(rol="Admin")
    usuario = Usuario.objects.create(username="usuario_prueba", correo="prueba@ejemplo.com", rol_id=rol)

    url = reverse('eliminar_usuario', args=[usuario.usuario_id])
    respuesta = cliente_admin.post(url)

    # Aserciones
    assert respuesta.status_code == 302  # Redirección después de la eliminación
    assert not Usuario.objects.filter(username="usuario_prueba").exists()

@pytest.mark.django_db
def test_vista_editar_usuario(cliente_admin):
    rol = Rol.objects.create(rol="Admin")
    usuario = Usuario.objects.create(username="usuario_prueba", correo="prueba@ejemplo.com", rol_id=rol)

    url = reverse('editar_usuario', args=[usuario.usuario_id])
    datos = {
        "username": "usuario_actualizado",
        "correo": "actualizado@ejemplo.com",
        "nombre": "Actualizado",
        "apellido": "Usuario",
        "rol_id": rol.rol_id,
        "password": "contraseña123"
    }

    respuesta = cliente_admin.post(url, datos)

    # Aserciones
    assert respuesta.status_code == 302  # Redirección después de la actualización
    usuario.refresh_from_db()
    assert usuario.username == "usuario_actualizado"
    assert usuario.correo == "actualizado@ejemplo.com"