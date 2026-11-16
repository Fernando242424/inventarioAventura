from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.forms import EstiloBootstrap
from .models import Perfil
from .utils import obtener_rol


class RegistroForm(EstiloBootstrap, UserCreationForm):
    telefono = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def save(self, commit=True):
        user = super().save()
        Perfil.objects.create(usuario=user, rol="turista", telefono=self.cleaned_data["telefono"])
        return user


class UsuarioForm(EstiloBootstrap, forms.ModelForm):
    rol = forms.ChoiceField(choices=Perfil.ROLES)
    telefono = forms.CharField(max_length=20, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False,
                            help_text="Obligatoria al crear. Al editar, vacía = no cambia.")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active"]
        labels = {"is_active": "Activo"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:                    
            self.fields["rol"].initial = obtener_rol(self.instance)
            perfil = getattr(self.instance, "perfil", None)
            self.fields["telefono"].initial = perfil.telefono if perfil else ""
        else:                                     
            self.fields["password"].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        user.save()
        Perfil.objects.update_or_create(
            usuario=user,
            defaults={"rol": self.cleaned_data["rol"], "telefono": self.cleaned_data["telefono"]})
        return user
