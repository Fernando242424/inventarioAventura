from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from cuentas.utils import obtener_rol
from experiencias.models import Categoria, Experiencia, Inscripcion


def inicio(request):
    return render(request, "core/inicio.html")


@login_required
def panel(request):
    rol = obtener_rol(request.user)
    datos = {}
    if rol == "admin":
        datos = {"usuarios": User.objects.count(),
                "categorias": Categoria.objects.count(),
                "experiencias": Experiencia.objects.count(),
                "reservas": Inscripcion.objects.count()}
    elif rol == "guia":
        datos = {"mis_experiencias": Experiencia.objects.filter(creador=request.user).count(),
                "mis_inscritos": Inscripcion.objects.filter(experiencia__creador=request.user).count()}
    else:
        datos = {"mis_reservas": Inscripcion.objects.filter(usuario=request.user).count(),
                "disponibles": Experiencia.objects.filter(activa=True, categoria__activo=True).count()}
    return render(request, "core/panel.html", datos)
