from django.db import models

# Create your models here.
class Temporizadores(models.Model):
    titulo = models.CharField(max_length=100)
    horas = models.IntegerField(default=0)
    minutos = models.IntegerField(default=25)
    segundos = models.IntegerField(default=0)
    uuid = models.IntegerField(default=0)
    prioridad = models.IntegerField(default=0)