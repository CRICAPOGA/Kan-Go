from django.db import models
from Proyectos.models import Proyecto

# Create your models here.
class Tarea(models.Model):
    tarea_id = models.AutoField(primary_key=True, verbose_name="Id")
    titulo = models.CharField(max_length=50, verbose_name="Tarea")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    estado = models.IntegerField(default=0, verbose_name="Estado")
    es_importante = models.BooleanField(default=False, verbose_name="¿Es importante?")
    es_urgente = models.BooleanField(default=False, verbose_name="¿Es urgente?")
    fecha_vencimiento = models.DateField(null=True, verbose_name="Fecha de vencimiento")
    proyecto_id = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name='Proyecto')

    def __str__(self):
        return self.titulo