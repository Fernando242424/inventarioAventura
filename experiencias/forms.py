from django import forms
from django.db.models import Q

from core.forms import EstiloBootstrap
from .models import Categoria, Experiencia


class CategoriaForm(EstiloBootstrap, forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "activo"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}


class ExperienciaForm(EstiloBootstrap, forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ["titulo", "descripcion", "precio", "cupo_maximo", "fecha_hora", "categoria", "activa"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "fecha_hora": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filtro = Q(activo=True)
        if self.instance.pk:
            filtro |= Q(pk=self.instance.categoria_id)
        self.fields["categoria"].queryset = Categoria.objects.filter(filtro)
        self.fields["fecha_hora"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M"
        ]