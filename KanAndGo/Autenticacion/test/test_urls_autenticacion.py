import pytest
from django.urls import reverse, resolve
from Autenticacion import views

@pytest.mark.django_db
def test_url_inicio_sesion():
    ruta = reverse('login_auth')
    assert resolve(ruta).func == views.login_auth

@pytest.mark.django_db
def test_url_cerrar_sesion():
    ruta = reverse('logout')
    assert resolve(ruta).func == views.logout_view

@pytest.mark.django_db
def test_url_registro():
    ruta = reverse('register')
    assert resolve(ruta).func == views.register_auth

@pytest.mark.django_db
def test_url_acceso():
    ruta = reverse('acceso')
    assert resolve(ruta).func == views.acceso