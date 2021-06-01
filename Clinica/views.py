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

'''class ListaUsuarios(generic.ListView):
    template_name = "pages/lista_usuarios.html"
    model = Usuario

class DetallesUsuario(generic.DetailView):
    template_name = "pages/detalles_usuario.html"
    model = Usuario'''

class NuevoUsuario(generic.CreateView):
    template_name = "pages/nuevo_usuario.html"
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy("Clinica:test")

'''class EditarUsuario(generic.UpdateView):
    template_name = "pages/editar_usuario.html"
    model = Usuario
    ##Faltaform_class =
    success_url = reverse_lazy("Clinica:detalles_usuario")

class ListaTratamiento(generic.ListView):
    template_name = "pages/lista_tratamientos.html"
    model =  Tratamiento

class CrearTratamiento(generic.CreateView):
    template_name = "pages/crear_tratamiento.html"
    model = Tratamiento
    #form_class = TratamientoForm ##Checar cuando a edy de la gana hacer este forms
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class EditarTratamiento(generic.UpdateView):
    template_name = "pages/editar_tratamiento.html"
    model = Tratamiento
    # Falta crear  form_class =
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class ListaDoctores(generic.ListView):
    template_name = "pages/lista_doctores.html"
    model = Doctor

class DetallesDoctor(generic.DetailView):
    template_name = template_name = "pages/detalles_doctor.html"
    model = Doctor
    success_url = reverse_lazy("Clinica:lista_doctores")

class ListaPacientes(generic.ListView):
    template_name = "pages/lista_pacientes.html"
    model =  ExpedientePaciente

class DetallesPaciente(generic.DetailView:
    template_name = "pages/detalles_paciente.html"
    model =  ExpedientePaciente
    success_url = reverse_lazy("Clinica:lista_pacientes")


class EditarPaciente(generic.UpdateView):
    template_name =  "pages/editar_paciente.html"
    model = ExpedientePaciente
    ##Form_class
    success_url = reverse_lazy("Clinica:lista_pacientes")

class ListaCitas(generic.ListView):
    template_name = "pages/lista_citas.html"
    model = Cita

class DetallesCita(generic.DetailView):
    template_name = "pages/detalles_cita.html"
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

class EditarCita(generic.UpdateView):
    template_name = "pages/editar_citas.html"
    model = Cita
    #form_class
    success_url = reverse_lazy("Clinica:lista_citas")

class PerfilDoctor(generic.DetailView):
    template_name = "pages/doctor.html"
    model = Doctor

class TramientosDoctor(generic.ListView):
    template_name = "pages/doctor_tratamientos.html"
    model = Tratamiento
    success_url = reverse_lazy("Clinica:doctor")

class HorarioDoctor(generic.ListView):
    template_name = "pages/horario_doctor.html"
    model = HorarioDoctor
    success_url = reverse_lazy("Clinica:doctor")

class EditarHorario(generic.UpdateView):
    template_name = "pages/editar_horario.html"
    model = HorarioDoctor
    #form_class
    success_url = reverse_lazy("Clinica:horario_doctor")

class CitasDoctor(generic.ListView):
    template_name = "pages/doctor_citas.html"
    model = Cita
    success_url = reverse_lazy("Clinica:doctor")

class VerNotas(generic.ListView):
    template_name = "pages/doctor_notas.html"
    model = Nota
    success_url = reverse_lazy("Clinica:doctor_citas")

class CrearNota(generic.CreateView):
    template_name = "pages/crear_notas.html"
    model = Nota
    #form_class
    success_url = reverse_lazy("Clinica:doctor_citas")

class VerPaciente(generic.DetailView):
    template_name = "pages/expedientepaciente.html"
    model = ExpedientePaciente
    success_url = reverse_lazy("Clinica:doctor_citas")'''
