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
HoraForms,EditarPacienteForm,CitaForm, EditarTratamientoForm, TratamientoForm, CitaForm

,FiltroUsuarios,FiltroTratamientos, FiltroPacientes)


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

#Consultar Usuarios
#Liga de donde lo consegui https://stackoverflow.com/questions/57554020/django-search-form-for-filtering
    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        # Do your filter and search here

        #CHEEEEECAR filtro all muestra a todos los tipos de usuario
        if filter_field == "all":
            return Usuario.objects.filter(
            (Q(Nombres__icontains=query) | Q(email__icontains=query) | (Q(TipoEmpleado__icontains=query) and ~Q(TipoEmpleado = 'A')))
            ).order_by("Nombres")
        elif filter_field == "Nombres":
            return Usuario.objects.filter(Q(TipoEmpleado='R') | Q(TipoEmpleado='D') and Q(Nombres__icontains=query)).order_by("Nombres")
        elif filter_field == "email":
            return Usuario.objects.filter(Q(TipoEmpleado='R') | Q(TipoEmpleado='D') and Q(email__icontains=query)).order_by("Nombres")
        elif filter_field == "TipoEmpleado":
            return Usuario.objects.filter(Q(TipoEmpleado='R') | Q(TipoEmpleado='D') and Q(TipoEmpleado__icontains=query)).order_by("Nombres")
        else:
            return Usuario.objects.filter(Q(TipoEmpleado='R') | Q(TipoEmpleado='D')).order_by("Nombres")



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroUsuarios(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })

        return context

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

class ListaTratamiento(LoginRequiredMixin,generic.ListView):
    template_name = "pages/lista_tratamientos.html"
    login_url = URL_LOGIN
    model =  Tratamiento

    def get_queryset(self):
        query = self.request.GET.get('search')
        # Do your filter and search here

        #CHEEEEECAR filtro all muestra a todos los tipos de usuario
        if not query:
            return Tratamiento.objects.all().order_by("Tratamiento")
        else:
            return Tratamiento.objects.filter(Q(Tratamiento__icontains=query)).order_by("Tratamiento")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroTratamientos(initial={
            'search': self.request.GET.get('search', ''),
        })

        return context

class EditarTratamiento(LoginRequiredMixin,generic.UpdateView):
    template_name = "pages/editar_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    form_class = EditarTratamientoForm
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class borrar_tratamiento(LoginRequiredMixin,generic.DeleteView):
    template_name = "pages/borrar_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class CrearTratamiento(LoginRequiredMixin,generic.CreateView):
    template_name = "pages/crear_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    form_class = TratamientoForm

#--------------VIEWS RECEPCIONISTA-------------

    ###____________________________________Pacientes____________________________________''
class ListaPacientes(LoginRequiredMixin,generic.ListView):
    template_name = "pages/lista_pacientes.html"
    login_url = URL_LOGIN
    model =  ExpedientePaciente

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        # Do your filter and search here

        #CHEEEEECAR filtro all muestra a todos los tipos de usuario
        if filter_field == "all":
            return ExpedientePaciente.objects.filter( Q(Nombres__icontains=query) | Q(email__icontains=query) | Q(Telefono__icontains=query)).order_by("Nombres")
        elif filter_field == "Nombres":
            return ExpedientePaciente.objects.filter(Q(Nombres__icontains=query) ).order_by("Nombres")
        elif filter_field == "email":
            return ExpedientePaciente.objects.filter(Q(email__icontains=query)).order_by("Nombres")
        elif filter_field == "Telefono":
            return ExpedientePaciente.objects.filter(Q(Telefono__icontains=query)).order_by("Nombres")
        else:
            return ExpedientePaciente.objects.all().order_by("Nombres")


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroPacientes(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })

        return context

class EditarPaciente(LoginRequiredMixin,generic.UpdateView):
    template_name =  "pages/editar_paciente.html"
    login_url = URL_LOGIN
    model = ExpedientePaciente
    form_class = EditarPacienteForm
    success_url = reverse_lazy("Clinica:lista_pacientes")

class DetallesPaciente(LoginRequiredMixin,generic.DetailView):
    template_name = "pages/detalles_paciente.html"
    login_url = URL_LOGIN
    model =  ExpedientePaciente
    success_url = reverse_lazy("Clinica:lista_pacientes")

class CrearPaciente(LoginRequiredMixin,generic.CreateView):
    template_name = "pages/crear_paciente.html"
    login_url = URL_LOGIN
    model = ExpedientePaciente
    form_class = ExpedientePacienteForm

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

class EditarHorario(generic.UpdateView): ###requiere pk de doctor, aun no funciona
    template_name = "pages/editar_horario.html"
    model = Hora
    form_class=HoraForms
    success_url = reverse_lazy("Clinica:horario_doctor")
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

class HorarioDoctor(generic.ListView):  ###Aun no hereda el form falta hacer  que acepte un pk de doctor aun no funciona
    template_name = "pages/horario_doctor.html"
    model = Hora
    success_url = reverse_lazy("Clinica:doctor")
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

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
