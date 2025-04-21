import pytest
from Proyectos.models import Proyecto
from Usuarios.models import Usuario
from django.utils.timezone import now

@pytest.mark.django_db
def test_creacion_proyecto():
    usuario = Usuario.objects.create(username="usuario_prueba", password="contraseña_prueba")
    proyecto = Proyecto.objects.create(
        nombre_proyecto="Proyecto Prueba",
        descripcion="Descripción del proyecto de prueba",
        estado=True,
        usuario_id=usuario
    )
    assert proyecto.nombre_proyecto == "Proyecto Prueba"
    assert proyecto.descripcion == "Descripción del proyecto de prueba"
    assert proyecto.estado is True
    assert proyecto.usuario_id == usuario

@pytest.mark.django_db
def test_metodo_str_proyecto():
    usuario = Usuario.objects.create(username="usuario_prueba", password="contraseña_prueba")
    proyecto = Proyecto.objects.create(
        nombre_proyecto="Proyecto Prueba",
        usuario_id=usuario
    )
    assert str(proyecto) == "Proyecto Prueba"

@pytest.mark.django_db
def test_fecha_creacion_proyecto_auto():
    usuario = Usuario.objects.create(username="usuario_prueba", password="contraseña_prueba")
    proyecto = Proyecto.objects.create(
        nombre_proyecto="Proyecto Prueba",
        usuario_id=usuario
    )
    assert proyecto.fecha_creacion is not None
    assert proyecto.fecha_creacion <= now()

@pytest.mark.django_db
def test_fecha_finalizacion_proyecto_nula():
    usuario = Usuario.objects.create(username="usuario_prueba", password="contraseña_prueba")
    proyecto = Proyecto.objects.create(
        nombre_proyecto="Proyecto Prueba",
        usuario_id=usuario
    )
    assert proyecto.fecha_finalizacion is None

@pytest.mark.django_db
def test_nombre_proyecto_unico():
    usuario = Usuario.objects.create(username="usuario_prueba", password="contraseña_prueba")
    Proyecto.objects.create(
        nombre_proyecto="Proyecto Prueba",
        usuario_id=usuario
    )
    with pytest.raises(Exception):
        Proyecto.objects.create(
            nombre_proyecto="Proyecto Prueba",
            usuario_id=usuario
        )