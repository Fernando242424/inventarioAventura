from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import confirmar_eliminar, guardar_formulario
from .forms import RegistroForm, UsuarioForm
from .utils import rol_requerido


class VistaLogin(LoginView):
    template_name = "cuentas/login.html"
    redirect_authenticated_user = True     

def registro(request):
    """Registro público de turistas."""
    form = RegistroForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Cuenta creada. Ya puedes iniciar sesión.")
        return redirect("login")
    return render(request, "cuentas/registro.html", {"form": form})


@rol_requerido("admin")
def usuario_lista(request):
    usuarios = User.objects.select_related("perfil").order_by("username")
    return render(request, "cuentas/usuario_lista.html", {"usuarios": usuarios})


@rol_requerido("admin")
def usuario_crear(request):
    return guardar_formulario(request, UsuarioForm(request.POST or None), "Nuevo usuario", "usuario_lista")


@rol_requerido("admin")
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    return guardar_formulario(request, UsuarioForm(request.POST or None, instance=usuario),
                            "Editar usuario", "usuario_lista")


@rol_requerido("admin")
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propio usuario.")
        return redirect("usuario_lista")
    return confirmar_eliminar(request, usuario, "usuario_lista")
