from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MaterialType(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialType, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    fecha_estimada = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ciudadano.username} - {self.material.nombre}"

class Solicitud(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En ruta'),
        ('completada', 'Completada'),
    ]

    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialType, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    fecha_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ciudadano.username} - {self.material.nombre}"
