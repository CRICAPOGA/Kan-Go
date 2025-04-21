import pytest
from django.urls import reverse, resolve
from Usuarios import views

@pytest.mark.django_db
def test_url_lista_usuarios():
    ruta = reverse('lista_usuarios')
    assert resolve(ruta).func == views.lista_usuarios

@pytest.mark.django_db
def test_url_crear_usuario():
    ruta = reverse('crear_usuario')
    assert resolve(ruta).func == views.crear_usuario

@pytest.mark.django_db
def test_url_editar_usuario():
    ruta = reverse('editar_usuario', kwargs={'usuario_id': 1})
    assert resolve(ruta).func == views.editar_usuario

@pytest.mark.django_db
def test_url_eliminar_usuario():
    ruta = reverse('eliminar_usuario', kwargs={'usuario_id': 1})
    assert resolve(ruta).func == views.eliminar_usuario