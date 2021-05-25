from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Expediente_Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora,
Doctor_Hora)

from .forms import UsuarioForm, ExpedientePacienteForm

# Create your views here.
class Index(generic.TemplateView):
    template_name = "pages/index.html"

# Logout temporal para que no mande error
class Login(generic.TemplateView):
    template_name = "pages/login.html"

class Test(generic.TemplateView):
    template_name = "pages/test.html"

class NuevoUsuario(generic.CreateView):
    template_name = "pages/nuevo_usuario.html"
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy("Clinica:test")
