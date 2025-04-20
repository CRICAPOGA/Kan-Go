import pytest
from Usuarios.models import Rol, Usuario
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_rol():
    rol = Rol.objects.create(rol="Admin")
    assert rol.rol == "Admin"
    assert str(rol) == "Admin"

@pytest.mark.django_db
def test_create_usuario():
    rol = Rol.objects.create(rol="Admin")
    usuario = Usuario.objects.create_user(
        username="testuser",
        password="testpassword",
        correo="testuser@example.com",
        nombre="Test",
        apellido="User",
        rol_id=rol
    )
    assert usuario.username == "testuser"
    assert usuario.check_password("testpassword")
    assert usuario.correo == "testuser@example.com"
    assert usuario.nombre == "Test"
    assert usuario.apellido == "User"
    assert usuario.rol_id == rol
    assert str(usuario) == "testuser"

@pytest.mark.django_db
def test_usuario_without_rol():
    usuario = Usuario.objects.create_user(
        username="noroluser",
        password="testpassword",
        correo="noroluser@example.com",
        nombre="No",
        apellido="Role"
    )
    assert usuario.username == "noroluser"
    assert usuario.rol_id is None