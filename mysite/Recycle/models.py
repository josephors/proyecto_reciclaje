from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=20)
    correo = models.CharField(max_length=30, unique=True)
    contrasena = models.CharField(max_length=30)
    id_evento= models.IntegerField(default=0)


    def __str__(self):
        return self.nombre 