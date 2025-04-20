import pytest
from Tareas.models import Tarea
from Proyectos.models import Proyecto
from Usuarios.models import Usuario
from datetime import date

@pytest.mark.django_db
def test_crear_tarea():
    usuario = Usuario.objects.create_user(
        username="usuario_tarea",
        password="contraseña123"
    )
    proyecto = Proyecto.objects.create(
        nombre_proyecto="Proyecto Prueba",
        descripcion="Descripción del proyecto",
        estado=True,
        usuario_id=usuario
    )
    tarea = Tarea.objects.create(
        titulo="Tarea Prueba",
        descripcion="Descripción de la tarea",
        estado=1,
        es_importante=True,
        es_urgente=False,
        fecha_vencimiento=date(2023, 12, 31),
        proyecto_id=proyecto
    )
    assert tarea.titulo == "Tarea Prueba"
    assert tarea.descripcion == "Descripción de la tarea"
    assert tarea.estado == 1
    assert tarea.es_importante is True
    assert tarea.es_urgente is False
    assert tarea.fecha_vencimiento == date(2023, 12, 31)
    assert tarea.proyecto_id == proyecto
    assert str(tarea) == "Tarea Prueba"

@pytest.mark.django_db
def test_tarea_valores_por_defecto():
    usuario = Usuario.objects.create_user(
        username="usuario_tarea_defecto",
        password="contraseña123"
    )
    proyecto = Proyecto.objects.create(
        nombre_proyecto="Proyecto Defecto",
        descripcion="Descripción del proyecto por defecto",
        estado=True,
        usuario_id=usuario
    )
    tarea = Tarea.objects.create(
        titulo="Tarea Defecto",
        proyecto_id=proyecto
    )
    assert tarea.estado == 0
    assert tarea.es_importante is False
    assert tarea.es_urgente is False
    assert tarea.fecha_vencimiento is None
    assert str(tarea) == "Tarea Defecto"

    def test_creacion_tarea(self):
        """Probar que una instancia de Tarea se crea correctamente."""
        self.assertEqual(self.tarea.titulo, "Tarea Prueba")
        self.assertEqual(self.tarea.descripcion, "Descripción de la tarea")
        self.assertEqual(self.tarea.estado, 1)
        self.assertTrue(self.tarea.es_importante)
        self.assertFalse(self.tarea.es_urgente)
        self.assertEqual(self.tarea.fecha_vencimiento, date(2023, 12, 31))
        self.assertEqual(self.tarea.proyecto_id, self.proyecto)

    def test_metodo_str_tarea(self):
        """Probar el método __str__ del modelo Tarea."""
        self.assertEqual(str(self.tarea), "Tarea Prueba")

    def test_valores_por_defecto_tarea(self):
        """Probar los valores por defecto del modelo Tarea."""
        tarea_defecto = Tarea.objects.create(
            titulo="Tarea Defecto",
            proyecto_id=self.proyecto
        )
        self.assertEqual(tarea_defecto.estado, 0)
        self.assertFalse(tarea_defecto.es_importante)
        self.assertFalse(tarea_defecto.es_urgente)
        self.assertIsNone(tarea_defecto.fecha_vencimiento)