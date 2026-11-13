from .utils import obtener_rol


def rol(request):
    """Context processor: deja la variable {{ rol }} disponible en todas las plantillas."""
    return {"rol": obtener_rol(request.user)}
