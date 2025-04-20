import pytest
from Usuarios.models import Rol, Usuario
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_crear_rol():
    rol = Rol.objects.create(rol="Admin")
    assert rol.rol == "Admin"
    assert str(rol) == "Admin"

@pytest.mark.django_db
def test_crear_usuario():
    rol = Rol.objects.create(rol="Admin")
    usuario = Usuario.objects.create_user(
        username="usuarioprueba",
        password="contraseñaprueba",
        correo="usuarioprueba@ejemplo.com",
        nombre="Prueba",
        apellido="Usuario",
        rol_id=rol
    )
    assert usuario.username == "usuarioprueba"
    assert usuario.check_password("contraseñaprueba")
    assert usuario.correo == "usuarioprueba@ejemplo.com"
    assert usuario.nombre == "Prueba"
    assert usuario.apellido == "Usuario"
    assert usuario.rol_id == rol
    assert str(usuario) == "usuarioprueba"

@pytest.mark.django_db
def test_usuario_sin_rol():
    usuario = Usuario.objects.create_user(
        username="usuariosinrol",
        password="contraseñaprueba",
        correo="usuariosinrol@ejemplo.com",
        nombre="Sin",
        apellido="Rol"
    )
    assert usuario.username == "usuariosinrol"
    assert usuario.rol_id is None