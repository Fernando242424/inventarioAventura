from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField("Fecha y hora de la actividad")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    creador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="experiencias_creadas")
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["fecha_hora"]

    def __str__(self):
        return self.titulo

    @property
    def cupos_disponibles(self):
        return self.cupo_maximo - self.inscripciones.count()


class Inscripcion(models.Model):
    ESTADOS = [("pendiente", "Pendiente"), ("confirmado", "Confirmado")]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inscripciones")
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=10, choices=ESTADOS, default="pendiente")

    class Meta:
        unique_together = ("usuario", "experiencia")  
        ordering = ["-fecha_inscripcion"]
        verbose_name = "inscripción"
        verbose_name_plural = "inscripciones"

    def __str__(self):
        return f"{self.usuario} -> {self.experiencia}"
