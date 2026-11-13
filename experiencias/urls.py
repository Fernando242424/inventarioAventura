from django.urls import path
from . import views as v

urlpatterns = [
    path("categorias/", v.categoria_lista, name="categoria_lista"),
    path("categorias/nueva/", v.categoria_crear, name="categoria_crear"),
    path("categorias/<int:pk>/editar/", v.categoria_editar, name="categoria_editar"),
    path("categorias/<int:pk>/eliminar/", v.categoria_eliminar, name="categoria_eliminar"),
    path("gestion/", v.experiencia_lista, name="experiencia_lista"),
    path("gestion/nueva/", v.experiencia_crear, name="experiencia_crear"),
    path("gestion/<int:pk>/editar/", v.experiencia_editar, name="experiencia_editar"),
    path("gestion/<int:pk>/eliminar/", v.experiencia_eliminar, name="experiencia_eliminar"),
    path("catalogo/", v.catalogo, name="catalogo"),
    path("catalogo/<int:pk>/inscribirse/", v.inscribirse, name="inscribirse"),
    path("reservas/", v.reserva_lista, name="reserva_lista"),
    path("reservas/<int:pk>/eliminar/", v.reserva_eliminar, name="reserva_eliminar"),
]
