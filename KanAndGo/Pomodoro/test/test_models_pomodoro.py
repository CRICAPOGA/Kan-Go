import pytest
from Pomodoro.models import Temporizadores, Sesiones
from Usuarios.models import Usuario
from Tareas.models import Tarea
from datetime import date, time

@pytest.mark.django_db
def test_temporizadores_creation():
    usuario = Usuario.objects.create(username="testuser", password="password123")
    temporizador = Temporizadores.objects.create(
        titulo="Test Timer",
        horas=1,
        minutos=30,
        segundos=0,
        uuid=12345,
        prioridad=1,
        usuario_id=usuario
    )
    assert temporizador.titulo == "Test Timer"
    assert temporizador.horas == 1
    assert temporizador.minutos == 30
    assert temporizador.segundos == 0
    assert temporizador.uuid == 12345
    assert temporizador.prioridad == 1
    assert temporizador.usuario_id == usuario

@pytest.mark.django_db
def test_temporizadores_str():
    temporizador = Temporizadores.objects.create(
        titulo="Test Timer",
        horas=1,
        minutos=30,
        segundos=0
    )
    assert str(temporizador) == "Test Timer1:30:0"
