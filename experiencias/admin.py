from django.contrib import admin
from .models import Categoria, Experiencia, Inscripcion

admin.site.register([Categoria, Experiencia, Inscripcion])
