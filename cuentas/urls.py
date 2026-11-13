from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.VistaLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),
    path("usuarios/", views.usuario_lista, name="usuario_lista"),
    path("usuarios/nuevo/", views.usuario_crear, name="usuario_crear"),
    path("usuarios/<int:pk>/editar/", views.usuario_editar, name="usuario_editar"),
    path("usuarios/<int:pk>/eliminar/", views.usuario_eliminar, name="usuario_eliminar"),
]
