from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    ROLES = [
        ("admin", "Administrador"),
        ("guia", "Guía / Operador"),
        ("turista", "Turista / Cliente"),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=10, choices=ROLES, default="turista")
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"
