from django.db import models
from Usuarios.models import Usuario
# Create your models here.
class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre_proyecto = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Proyecto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    estado = models.BooleanField(default=False, verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_finalizacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Finalización")
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return self.nombre_proyecto