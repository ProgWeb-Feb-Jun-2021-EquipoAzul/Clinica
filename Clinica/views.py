from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora,
Doctor_Hora)

from .forms import UsuarioForm, ExpedientePacienteForm, NotaForm,CitaForm,DoctorForm

# Create your views here.
class Index(generic.TemplateView):
    template_name = "pages/index.html"

class NuevoUsuario(generic.CreateView):
    template_name = "pages/nuevo_usuario.html"
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy("Clinica:test")
