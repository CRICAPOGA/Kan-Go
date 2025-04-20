from django.test import TestCase
from Tareas.models import Tarea
from Proyectos.models import Proyecto
from Usuarios.models import Usuario
from datetime import date

class TareaModelTest(TestCase):
    def setUp(self):
        # Create a mock user
        self.usuario = Usuario.objects.create(
            username="testuser",
            password="password123"
        )
        # Create a mock project
        self.proyecto = Proyecto.objects.create(
            nombre_proyecto="Proyecto Test",
            descripcion="Descripción del proyecto",
            estado=True,
            usuario_id=self.usuario
        )
        # Create a mock task
        self.tarea = Tarea.objects.create(
            titulo="Tarea Test",
            descripcion="Descripción de la tarea",
            estado=1,
            es_importante=True,
            es_urgente=False,
            fecha_vencimiento=date(2023, 12, 31),
            proyecto_id=self.proyecto
        )

    def test_tarea_creation(self):
        """Test that a Tarea instance is created correctly."""
        self.assertEqual(self.tarea.titulo, "Tarea Test")
        self.assertEqual(self.tarea.descripcion, "Descripción de la tarea")
        self.assertEqual(self.tarea.estado, 1)
        self.assertTrue(self.tarea.es_importante)
        self.assertFalse(self.tarea.es_urgente)
        self.assertEqual(self.tarea.fecha_vencimiento, date(2023, 12, 31))
        self.assertEqual(self.tarea.proyecto_id, self.proyecto)

    def test_tarea_str_method(self):
        """Test the __str__ method of the Tarea model."""
        self.assertEqual(str(self.tarea), "Tarea Test")

    def test_tarea_default_values(self):
        """Test the default values of the Tarea model."""
        tarea_default = Tarea.objects.create(
            titulo="Tarea Default",
            proyecto_id=self.proyecto
        )
        self.assertEqual(tarea_default.estado, 0)
        self.assertFalse(tarea_default.es_importante)
        self.assertFalse(tarea_default.es_urgente)
        self.assertIsNone(tarea_default.fecha_vencimiento)