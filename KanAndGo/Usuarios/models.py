from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    rol_id = models.AutoField(primary_key=True, verbose_name="Id")
    rol = models.CharField(max_length=30, verbose_name="Role")

    def __str__(self):
        return self.rol

class Usuario(AbstractUser):
    usuario_id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido")
    username = models.CharField(max_length=50, unique=True, verbose_name="Username")
    correo = models.EmailField(unique=True, verbose_name="Correo")
    role_id = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name='Rol', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo', 'nombre', 'apellido']

    def __str__(self):
        return self.username