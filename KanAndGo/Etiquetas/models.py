from django.db import models
from Usuarios.models import Usuario
from Tareas.models import Tarea

# Create your models here.
class Etiqueta(models.Model):
    etiqueta_id = models.AutoField(primary_key=True, verbose_name="Id")
    etiqueta = models.CharField(max_length=50, unique=True, verbose_name="Etiqueta")
    color = models.CharField(max_length=6, blank=True, null=True, verbose_name="Color") # En hexadecimal
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return self.etiqueta

class DetalleEtiqueta(models.Model):
    detalle_etiqueta_id = models.AutoField(primary_key=True, verbose_name="Id")
    etiqueta_id = models.ForeignKey(Etiqueta, on_delete=models.CASCADE, verbose_name='Etiqueta')
    tarea_id = models.ForeignKey(Tarea, on_delete=models.CASCADE, verbose_name='Tarea')

    def __str__(self):
        return f"Detalle de Etiqueta {self.detalle_etiqueta_id}: {self.etiqueta_id.etiqueta} - {self.tarea_id.titulo}"