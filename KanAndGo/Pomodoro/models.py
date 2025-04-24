from django.db import models
from Usuarios.models import Usuario

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