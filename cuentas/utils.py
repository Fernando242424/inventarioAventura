from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def obtener_rol(user):
    if not user.is_authenticated:
        return None
    perfil = getattr(user, "perfil", None)
    if perfil:
        return perfil.rol
    return "admin" if user.is_superuser else "turista"   

def rol_requerido(*roles):
    def decorador(vista):
        @login_required
        @wraps(vista)
        def envuelta(request, *args, **kwargs):
            if obtener_rol(request.user) not in roles:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return envuelta
    return decorador
