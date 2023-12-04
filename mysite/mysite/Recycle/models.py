from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#class Usuario(models.Model):
#    nombre = models.CharField(max_length=20)
#    username = models.CharField(max_length=30, unique=True)
#    password = models.CharField(max_length=30)

#    def __str__(self):
#        return self.nombre 


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=20)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    #last_login = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_groups',  # Cambia 'custom_user_groups' según tus necesidades
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',  # Cambia 'custom_user_permissions' según tus necesidades
    )

    def __str__(self):
        return self.nombre