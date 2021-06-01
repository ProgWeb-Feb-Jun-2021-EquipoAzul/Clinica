from django.contrib import admin
from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora)

# Register your models here.
admin.site.register(Usuario)
admin.site.register(ExpedientePaciente)
admin.site.register(Doctor)
admin.site.register(Nota)
admin.site.register(Cita)
admin.site.register(Tratamiento)
admin.site.register(Doctor_Tratamiento)
admin.site.register(Hora)
