from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect, render


def confirmar_eliminar(request, objeto, destino):
    if request.method == "POST":
        try:
            objeto.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: tiene registros asociados.")
        return redirect(destino)
    return render(request, "confirmar_eliminar.html", {"objeto": objeto, "volver": destino})


def guardar_formulario(request, form, titulo, destino):
    if form.is_valid():
        form.save()
        messages.success(request, "Guardado correctamente.")
        return redirect(destino)
    return render(request, "form.html", {"form": form, "titulo": titulo, "volver": destino})
