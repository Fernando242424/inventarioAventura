from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import confirmar_eliminar, guardar_formulario
from cuentas.utils import obtener_rol, rol_requerido
from .forms import CategoriaForm, ExperienciaForm
from .models import Categoria, Experiencia, Inscripcion


# ---------- CATEGORÍAS: solo Administrador ----------
# Si cambias de tema: renombra Categoria / categoria_* por tu modelo.
@rol_requerido("admin")
def categoria_lista(request):
    categorias = Categoria.objects.annotate(total=Count("experiencia"))
    return render(request, "experiencias/categoria_lista.html", {"categorias": categorias})


@rol_requerido("admin")
def categoria_crear(request):
    return guardar_formulario(request, CategoriaForm(request.POST or None), "Nueva categoría", "categoria_lista")


@rol_requerido("admin")
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return guardar_formulario(request, CategoriaForm(request.POST or None, instance=categoria),
                              "Editar categoría", "categoria_lista")


@rol_requerido("admin")
def categoria_eliminar(request, pk):
    return confirmar_eliminar(request, get_object_or_404(Categoria, pk=pk), "categoria_lista")


# ---------- EXPERIENCIAS: admin todas, guía solo las suyas ----------
def mis_experiencias(request):
    if obtener_rol(request.user) == "admin":
        return Experiencia.objects.all()
    return Experiencia.objects.filter(creador=request.user)   # restricción del guía


@rol_requerido("admin", "guia")
def experiencia_lista(request):
    experiencias = mis_experiencias(request).annotate(total_inscritos=Count("inscripciones"))
    return render(request, "experiencias/experiencia_lista.html", {"experiencias": experiencias})


@rol_requerido("admin", "guia")
def experiencia_crear(request):
    form = ExperienciaForm(request.POST or None)
    form.instance.creador = request.user          # el creador es quien la registra
    return guardar_formulario(request, form, "Nueva experiencia", "experiencia_lista")


@rol_requerido("admin", "guia")
def experiencia_editar(request, pk):
    experiencia = get_object_or_404(mis_experiencias(request), pk=pk)   # ajena -> 404
    return guardar_formulario(request, ExperienciaForm(request.POST or None, instance=experiencia),
                              "Editar experiencia", "experiencia_lista")


@rol_requerido("admin")          # el guía NO elimina
def experiencia_eliminar(request, pk):
    return confirmar_eliminar(request, get_object_or_404(Experiencia, pk=pk), "experiencia_lista")


# ---------- CATÁLOGO E INSCRIPCIÓN ----------
@login_required
def catalogo(request):
    experiencias = (Experiencia.objects.filter(activa=True, categoria__activo=True)
                    .annotate(total_inscritos=Count("inscripciones")))
    inscritas = Inscripcion.objects.filter(usuario=request.user).values_list("experiencia_id", flat=True)
    return render(request, "experiencias/catalogo.html",
                  {"experiencias": experiencias, "inscritas": list(inscritas)})


@rol_requerido("turista")
def inscribirse(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk, activa=True, categoria__activo=True)
    if request.method == "POST":
        if Inscripcion.objects.filter(usuario=request.user, experiencia=experiencia).exists():
            messages.warning(request, "Ya estás inscrito en esta experiencia.")
        elif experiencia.cupos_disponibles <= 0:
            messages.error(request, "No quedan cupos disponibles.")
        else:
            Inscripcion.objects.create(usuario=request.user, experiencia=experiencia)
            messages.success(request, "¡Inscripción realizada!")
    return redirect("catalogo")


# ---------- RESERVAS: admin todas, turista las suyas ----------
def mis_reservas(request):
    if obtener_rol(request.user) == "admin":
        return Inscripcion.objects.all()
    return Inscripcion.objects.filter(usuario=request.user)


@rol_requerido("admin", "turista")
def reserva_lista(request):
    return render(request, "experiencias/reserva_lista.html", {"reservas": mis_reservas(request)})


@rol_requerido("admin", "turista")
def reserva_eliminar(request, pk):
    reserva = get_object_or_404(mis_reservas(request), pk=pk)
    return confirmar_eliminar(request, reserva, "reserva_lista")
