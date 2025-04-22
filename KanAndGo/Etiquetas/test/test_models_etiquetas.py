import pytest
from Etiquetas.models import Etiqueta, DetalleEtiqueta
from Usuarios.models import Usuario
from Tareas.models import Tarea
from Proyectos.models import Proyecto

@pytest.mark.django_db
def test_crear_etiqueta():
    usuario = Usuario.objects.create_user(username="usuario_prueba", password="contraseña123", correo="prueba@example.com", nombre="Prueba", apellido="Usuario")
    etiqueta = Etiqueta.objects.create(etiqueta="Urgente", color="FF0000", usuario_id=usuario)
    assert etiqueta.etiqueta == "Urgente"
    assert etiqueta.color == "FF0000"
    assert etiqueta.usuario_id == usuario

@pytest.mark.django_db
def test_crear_detalle_etiqueta():
    usuario = Usuario.objects.create_user(username="usuario_prueba", password="contraseña123", correo="prueba@example.com", nombre="Prueba", apellido="Usuario")
    proyecto = Proyecto.objects.create(nombre_proyecto="Proyecto 1", usuario_id=usuario)
    tarea = Tarea.objects.create(titulo="Tarea 1", proyecto_id=proyecto)
    etiqueta = Etiqueta.objects.create(etiqueta="Importante", color="00FF00", usuario_id=usuario)
    detalle_etiqueta = DetalleEtiqueta.objects.create(etiqueta_id=etiqueta, tarea_id=tarea)
    assert detalle_etiqueta.etiqueta_id == etiqueta
    assert detalle_etiqueta.tarea_id == tarea

@pytest.mark.django_db
def test_etiqueta_str():
    usuario = Usuario.objects.create_user(username="usuario_prueba", password="contraseña123", correo="prueba@example.com", nombre="Prueba", apellido="Usuario")
    etiqueta = Etiqueta.objects.create(etiqueta="Revisión", color="0000FF", usuario_id=usuario)
    assert str(etiqueta) == "Revisión"

@pytest.mark.django_db
def test_detalle_etiqueta_str():
    usuario = Usuario.objects.create_user(username="usuario_prueba", password="contraseña123", correo="prueba@example.com", nombre="Prueba", apellido="Usuario")
    proyecto = Proyecto.objects.create(nombre_proyecto="Proyecto 1", usuario_id=usuario)
    tarea = Tarea.objects.create(titulo="Corregir error", proyecto_id=proyecto)
    etiqueta = Etiqueta.objects.create(etiqueta="Bug", color="FFFF00", usuario_id=usuario)
    detalle_etiqueta = DetalleEtiqueta.objects.create(etiqueta_id=etiqueta, tarea_id=tarea)
    assert str(detalle_etiqueta) == f"Detalle de Etiqueta {detalle_etiqueta.detalle_etiqueta_id}: Bug - Corregir error"