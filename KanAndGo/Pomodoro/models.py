from django.db import models
from Usuarios.models import Usuario
from Tareas.models import Tarea

# Create your models here.
class Temporizadores(models.Model):
    titulo = models.CharField(max_length=100)
    horas = models.IntegerField(default=0)
    minutos = models.IntegerField(default=25)
    segundos = models.IntegerField(default=0)
    uuid = models.IntegerField(default=0)
    prioridad = models.IntegerField(default=0)
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario', null=True, blank=True)

    def __str__(self):
        return self.titulo + str(self.horas) + ':' + str(self.minutos) + ':' + str(self.segundos)

class Sesiones(models.Model):
    tarea_id = models.ForeignKey(Tarea, on_delete=models.CASCADE, verbose_name='Tarea', null=True, blank=True)
    sesiones = models.IntegerField(default=0)
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha')
    hora = models.TimeField(auto_now_add=True, verbose_name='Hora')

    def __str__(self):
        return str(self.tarea_id) + ' - ' + str(self.sesiones)
    