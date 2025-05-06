import pytest
from django.urls import reverse, resolve
from Autenticacion import views
from django.contrib.auth import views as auth_views

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

@pytest.mark.django_db
def test_url_reset_password():
    ruta = reverse('password_reset')
    assert resolve(ruta).func.view_class == auth_views.PasswordResetView

@pytest.mark.django_db
def test_url_reset_password_sent():
    ruta = reverse('password_reset_done')
    assert resolve(ruta).func.view_class == auth_views.PasswordResetDoneView

@pytest.mark.django_db
def test_url_reset_password_confirm():
    ruta = reverse('password_reset_confirm', kwargs={'uidb64': 'uid', 'token': 'token'})
    assert resolve(ruta).func.view_class == auth_views.PasswordResetConfirmView

@pytest.mark.django_db
def test_url_reset_password_complete():
    ruta = reverse('password_reset_complete')
    assert resolve(ruta).func.view_class == auth_views.PasswordResetCompleteView