# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Solicitud(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En ruta'),
        ('completada', 'Completada'),
    ]
    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey('MaterialType', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    fecha_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    operario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_asignadas'
    )
    fecha_completada = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ciudadano.username} - {self.material.nombre}"

class Comentario(models.Model):
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.CASCADE, related_name='comentarios'
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} en solicitud {self.solicitud.id}"

class MaterialType(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class PuntoLimpio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    horario = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Recomendacion(models.Model):
    titulo = models.CharField(max_length=100)
    texto = models.TextField()

    def __str__(self):
        return self.titulo
