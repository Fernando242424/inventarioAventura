from .utils import obtener_rol


def rol(request):
    return {"rol": obtener_rol(request.user)}
