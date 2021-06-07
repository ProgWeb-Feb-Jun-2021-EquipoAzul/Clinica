from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora)

from .forms import (NuevoUsuarioForm, EditarUsuarioForm, ExpedientePacienteForm, NotaForm, CitaForm, DoctorForm,
HoraForms,EditarPacienteForm,CitaForm, EditarTratamientoForm, TratamientoForm, CitaForm)


URL_LOGIN='login'


#-----------------VIEWS GENERALES-----------------

class Index(LoginRequiredMixin, generic.TemplateView):
    template_name = "pages/index.html"
    login_url = URL_LOGIN

#--------------VIEWS ADMINISTRADOR-------------

    ###____________________________________Usuarios________________________________________''
class ListaUsuarios(LoginRequiredMixin,generic.ListView):
    template_name = "pages/lista_usuarios.html"
    login_url = URL_LOGIN
    queryset = Usuario.objects.filter(Q(TipoEmpleado='R') | Q(TipoEmpleado='D')).order_by("Nombres")

class NuevoUsuario(LoginRequiredMixin,generic.CreateView):
    template_name = "pages/nuevo_usuario.html"
    login_url = URL_LOGIN
    model = Usuario
    form_class = NuevoUsuarioForm
    success_url = reverse_lazy("Clinica:index")

class EditarUsuario(LoginRequiredMixin,generic.UpdateView):
    template_name = "pages/editar_usuario.html"
    login_url = URL_LOGIN
    model = Usuario
    form_class = EditarUsuarioForm
    success_url = reverse_lazy("Clinica:lista_usuarios")

class DetallesUsuario(LoginRequiredMixin,generic.DetailView):
    template_name = "pages/detalles_usuario.html"
    login_url = URL_LOGIN
    model = Usuario

class BorrarUsuario(LoginRequiredMixin,generic.DeleteView):
    template_name = "pages/borrar_usuario.html"
    login_url = URL_LOGIN
    model = Usuario
    success_url = reverse_lazy("Clinica:lista_usuarios")
    ###____________________________________Tratamientos________________________________________''

class ListaTratamiento(generic.ListView):
    template_name = "pages/lista_tratamientos.html"
    model =  Tratamiento

class EditarTratamiento(generic.UpdateView):
    template_name = "pages/editar_tratamiento.html"
    model = Tratamiento
    form_class = EditarTratamientoForm
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class borrar_tratamiento(LoginRequiredMixin,generic.DeleteView):
    template_name = "pages/borrar_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class CrearTratamiento(generic.CreateView):
    template_name = "pages/crear_tratamiento.html"
    model = Tratamiento
    form_class = TratamientoForm

#--------------VIEWS RECEPCIONISTA-------------

    ###____________________________________Pacientes____________________________________''
class ListaPacientes(generic.ListView):
    template_name = "pages/lista_pacientes.html"
    model =  ExpedientePaciente

class EditarPaciente(generic.UpdateView):
    template_name =  "pages/editar_paciente.html"
    model = ExpedientePaciente
    form_class = EditarPacienteForm
    success_url = reverse_lazy("Clinica:lista_pacientes")

class DetallesPaciente(generic.DetailView):
    template_name = "pages/detalles_paciente.html"
    model =  ExpedientePaciente
    success_url = reverse_lazy("Clinica:lista_pacientes")

#Falta crear pacientes

    ###_____________________________Citas_________________________________________
class ListaCitas(generic.ListView):
    template_name = "pages/lista_citas.html"
    model = Cita

#Falta crear citas desde pacientes

class CrearCita(generic.CreateView):
    template_name = "pages/crear_cita.html"
    model =  Cita
    form_class = CitaForm
    success_url = reverse_lazy("Clinica:lista_citas")
class DetallesCita(generic.DetailView):
    template_name = "pages/detalles_cita.html"
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

class EditarCita(generic.UpdateView):
    template_name = "pages/editar_cita.html"
    model = Cita
    form_class=CitaForm
    success_url = reverse_lazy("Clinica:lista_citas")

class BorrarCita(LoginRequiredMixin,generic.DeleteView): ###Falta completar
    template_name = "pages/borrar_cita.html"
    login_url = URL_LOGIN
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

    ###_____________________________Doctores_________________________________________
class ListaDoctores(generic.ListView):
    template_name = "pages/lista_doctores.html"
    model = Doctor

class DetallesDoctor(generic.DetailView):
    template_name = "pages/detalles_doctor.html"
    model = Doctor
    success_url = reverse_lazy("Clinica:lista_doctores")

#-----------------VIEWS DOCTOR-----------------

    ###_____________________________Perfil_________________________________________
'''#No implementado
class PerfilDoctor(generic.DetailView):
    template_name = "pages/doctor.html"
    model = Doctor
'''
    ###_____________________________Tratamientos___________________________________
'''#No implementa
class TramientosDoctor(generic.ListView):
    template_name = "pages/doctor_tratamientos.html"
    model = Tratamiento
    success_url = reverse_lazy("Clinica:doctor")
'''

    ###_____________________________Horario___________________________________
#Mas o menos implementado solo debe de dejar entrar a doctores
class AgregarHorario(generic.CreateView):
    template_name = "pages/agregar_horario.html"
    model = Hora
    form_class = HoraForms
    success_url = reverse_lazy("Clinica:index")

    #Agrega la pk de doctor a la que pertenece la hora agregada
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)



'''#No implementado
class EditarHorario(generic.UpdateView):
    template_name = "pages/editar_horario.html"
    model = HorarioDoctor
    #form_class
    success_url = reverse_lazy("Clinica:horario_doctor")
'''

'''#No implementado
class HorarioDoctor(generic.ListView):
    template_name = "pages/horario_doctor.html"
    model = HorarioDoctor
    success_url = reverse_lazy("Clinica:doctor")
'''
    ###_____________________________Citas___________________________________
'''#No implementado
class CitasDoctor(generic.ListView):
    template_name = "pages/doctor_citas.html"
    model = Cita
    success_url = reverse_lazy("Clinica:doctor")
'''

'''#No implementado
class VerPaciente(generic.DetailView):
    template_name = "pages/expedientepaciente.html"
    model = ExpedientePaciente
    success_url = reverse_lazy("Clinica:doctor_citas")
'''

        ###_____________________________Notas___________________________________
#path('doctor_notas', views.VerNotas.as_view(), name="doctor_notas"), #No implementado #Ver notas del paciente
#path('crear_notas', views.CrearNota.as_view(), name="crear_notas"), #No implementado #Crear nota al paciente

'''#No implementado
class VerNotas(generic.ListView):
    template_name = "pages/doctor_notas.html"
    model = Nota
    success_url = reverse_lazy("Clinica:doctor_citas")
'''

'''#No implementado
class CrearNota(generic.CreateView):
    template_name = "pages/crear_notas.html"
    model = Nota
    #form_class
    success_url = reverse_lazy("Clinica:doctor_citas")
'''
