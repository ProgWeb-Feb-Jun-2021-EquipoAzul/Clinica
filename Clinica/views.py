from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

from django.contrib.auth import views as auth_views


#Importamos todos los modelos de models.py del app Clinica
from .models import *
#Importamos todos los forms de forms.py del app Clinica
from .forms import *


URL_LOGIN='Clinica:login'

#-----------------CLASES PRIVILEGIOS-----------------

#Clase que se utiliza para comprobar si el usuario es un recepcionista
class TestRecepcionistaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.TipoEmpleado == "R"

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('Clinica:login'))
        return HttpResponseRedirect(reverse_lazy('Clinica:redirect'))

#Clase que se utiliza para comprobar si el usuario es un doctor
class TestDoctorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.TipoEmpleado == "D"

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('Clinica:login'))
        return HttpResponseRedirect(reverse_lazy('Clinica:redirect'))

#Clase que se utiliza para comprobar si el usuario es un administrador
class TestAdministradorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.TipoEmpleado == "A"

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('Clinica:login'))
        return HttpResponseRedirect(reverse_lazy('Clinica:redirect'))

#-----------------VIEWS GENERALES-----------------


class Redirect(generic.TemplateView):
    template_name = "pages/redirect.html"

#Login con redireccion a la pagina principal de cada usuario
class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    #Cuando abre el login si el usuario esta autenticado automaticamente te redirecciona a la pagina principal de cada uno
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.TipoEmpleado == "R":
                return HttpResponseRedirect(reverse_lazy('Clinica:lista_citas'))
            elif self.request.user.TipoEmpleado == "D":
                return HttpResponseRedirect(reverse_lazy('Clinica:doctor_citas'))
            elif self.request.user.TipoEmpleado == "A":
                return HttpResponseRedirect(reverse_lazy('Clinica:lista_usuarios'))
        return super(LoginView, self).get(request, *args, **kwargs)

    #Cuando el login es exitosos redirecciona a una de estas 3 paginas dependiendo que tipo de empleado es
    def get_success_url(self):
        if self.request.user.TipoEmpleado == "R":
            return reverse_lazy('Clinica:lista_citas')
        elif self.request.user.TipoEmpleado == "D":
            return reverse_lazy('Clinica:doctor_citas')
        elif self.request.user.TipoEmpleado == "A":
            return reverse_lazy('Clinica:lista_usuarios')

#--------------VIEWS ADMINISTRADOR-------------

    ###____________________________________Usuarios________________________________________''
class ListaUsuarios(TestDoctorMixin, generic.ListView):
    template_name = "pages/lista_usuarios.html"

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

class NuevoUsuario(TestAdministradorMixin, TestRecepcionistaMixin,generic.CreateView):
    template_name = "pages/nuevo_usuario.html"
    model = Usuario
    form_class = NuevoUsuarioForm
    success_url = reverse_lazy("Clinica:index")

class EditarUsuario(TestAdministradorMixin, generic.UpdateView):
    template_name = "pages/editar_usuario.html"
    model = Usuario
    form_class = EditarUsuarioForm
    success_url = reverse_lazy("Clinica:lista_usuarios")

class DetallesUsuario(TestAdministradorMixin, generic.DetailView):
    template_name = "pages/detalles_usuario.html"
    model = Usuario

class BorrarUsuario(TestAdministradorMixin, generic.DeleteView):
    template_name = "pages/borrar_usuario.html"
    model = Usuario
    success_url = reverse_lazy("Clinica:lista_usuarios")
    ###____________________________________Tratamientos________________________________________''

class ListaTratamiento(TestAdministradorMixin, generic.ListView):
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

class EditarTratamiento(TestAdministradorMixin, generic.UpdateView):
    template_name = "pages/editar_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    form_class = EditarTratamientoForm
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class borrar_tratamiento(TestAdministradorMixin, generic.DeleteView):
    template_name = "pages/borrar_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    success_url = reverse_lazy("Clinica:lista_tratamientos")

class CrearTratamiento(TestAdministradorMixin, generic.CreateView):
    template_name = "pages/crear_tratamiento.html"
    login_url = URL_LOGIN
    model = Tratamiento
    form_class = TratamientoForm
    success_url = reverse_lazy("Clinica:lista_tratamientos")

#--------------VIEWS RECEPCIONISTA-------------

    ###____________________________________Pacientes____________________________________''
class ListaPacientes(TestRecepcionistaMixin, generic.ListView):
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

class EditarPaciente(TestRecepcionistaMixin, generic.UpdateView):
    template_name =  "pages/editar_paciente.html"
    login_url = URL_LOGIN
    model = ExpedientePaciente
    form_class = EditarPacienteForm
    success_url = reverse_lazy("Clinica:lista_pacientes")

class DetallesPaciente(TestRecepcionistaMixin, generic.DetailView):
    template_name = "pages/detalles_paciente.html"
    login_url = URL_LOGIN
    model =  ExpedientePaciente
    success_url = reverse_lazy("Clinica:lista_pacientes")

class CrearPaciente(TestRecepcionistaMixin, generic.CreateView):
    template_name = "pages/crear_paciente.html"
    login_url = URL_LOGIN
    model = ExpedientePaciente
    form_class = ExpedientePacienteForm
    success_url = reverse_lazy("Clinica:lista_pacientes")

    ###_____________________________Citas_________________________________________
class ListaCitas(TestRecepcionistaMixin, generic.ListView):
    template_name = "pages/lista_citas.html"
    login_url = URL_LOGIN
    model = Cita

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        # Do your filter and search here
        if filter_field == "all":
            return Cita.objects.filter(Q(ExpedientePaciente__Nombres__icontains=query)|Q(Doctor__Usuario__Nombres__icontains=query)|Q(Fecha__icontains=query)).order_by("ExpedientePaciente__Nombres")
        elif filter_field == "Paciente":
            return Cita.objects.filter(Q(ExpedientePaciente__Nombres__icontains=query)).order_by("ExpedientePaciente__Nombres")
        elif filter_field == "Doctor":
            return Cita.objects.filter(Q(Doctor__Usuario__Nombres__icontains=query)).order_by("ExpedientePaciente__Nombres")
        elif filter_field == "Fecha":
            return Cita.objects.filter(Q(Fecha__icontains=query)).order_by("ExpedientePaciente__Nombres")
        else:
            return Cita.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroCitas(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })

        return context

#Falta crear citas desde pacientes

class CrearCita(TestRecepcionistaMixin, generic.CreateView):
    template_name = "pages/crear_cita.html"
    login_url = URL_LOGIN
    model =  Cita
    form_class = CitaForm
    success_url = reverse_lazy("Clinica:lista_citas")
class DetallesCita(TestRecepcionistaMixin, generic.DetailView):
    template_name = "pages/detalles_cita.html"
    login_url = URL_LOGIN
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

class EditarCita(TestRecepcionistaMixin, generic.UpdateView):
    template_name = "pages/editar_cita.html"
    login_url = URL_LOGIN
    model = Cita
    form_class=EditarCitaForm
    success_url = reverse_lazy("Clinica:lista_citas")

class BorrarCita(TestRecepcionistaMixin, generic.DeleteView): ###Falta completar
    template_name = "pages/borrar_cita.html"
    login_url = URL_LOGIN
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

    ###_____________________________Doctores_________________________________________
class ListaDoctores(TestDoctorMixin, generic.ListView):
    template_name = "pages/lista_doctores.html"
    login_url = URL_LOGIN
    model = Doctor

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        # Do your filter and search here

        #CHEEEEECAR filtro all muestra a todos los tipos de usuario
        if filter_field == "all":
            return Doctor.objects.filter(Q(Usuario__Nombres__icontains=query) | Q(Especialidad__icontains=query)| Q(Usuario__email__icontains=query)| Q(Usuario__Telefono__icontains=query)).order_by("Usuario__Nombres")
        elif filter_field == "Nombres":
            return Doctor.objects.filter(Q(Usuario__Nombres__icontains=query) ).order_by("Usuario__Nombres")
        elif filter_field == "Especialidad":
            return Doctor.objects.filter(Q(Especialidad__icontains=query)).order_by("Usuario__Nombres")
        elif filter_field == "Correo":
            return Doctor.objects.filter(Q(Usuario__email__icontains=query)).order_by("Usuario__Nombres")
        elif filter_field == "Telefono":
            return Doctor.objects.filter(Q(Usuario__Telefono__icontains=query)).order_by("Usuario__Nombres")
        else:
            return Doctor.objects.all().order_by("Usuario__Nombres")


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroDoctores(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })

        return context

class DetallesDoctor(TestDoctorMixin, generic.DetailView):
    template_name = "pages/detalles_doctor.html"
    login_url = URL_LOGIN
    model = Doctor
    success_url = reverse_lazy("Clinica:lista_doctores")

#-----------------VIEWS DOCTOR-----------------
    ###_____________________________Perfil_________________________________________
#No implementado
class PerfilDoctor(TestDoctorMixin, generic.DetailView):
    template_name = "pages/perfil.html"
    login_url = URL_LOGIN
    model = Doctor

class EditarPerfil(TestDoctorMixin, generic.UpdateView):
    template_name = "pages/editar_perfil.html"
    login_url = URL_LOGIN
    model = Doctor
    form_class=PerfilDoctorForm

    def get_success_url(self):
          doctor=self.kwargs['pk']
          return reverse_lazy('Clinica:perfil', kwargs={'pk': doctor})

    ###_____________________________Horario___________________________________
#Mas o menos implementado solo debe de dejar entrar a doctores
class AgregarHorario(TestDoctorMixin, generic.CreateView):
    template_name = "pages/agregar_horario.html"
    login_url = URL_LOGIN
    model = Hora
    form_class = HoraForms
    success_url = reverse_lazy("Clinica:horario")

    #Agrega la pk de doctor a la que pertenece la hora agregada
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

class DetallesCitaDoctor(TestDoctorMixin, generic.DetailView):
    template_name = "pages/detalles_cita_doctor.html"
    login_url = URL_LOGIN
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

class EditarHorario(TestDoctorMixin, generic.UpdateView):
    template_name = "pages/editar_horario.html"
    login_url = URL_LOGIN
    model = Hora
    form_class=EditarHoraForms
    success_url = reverse_lazy("Clinica:horario_doctor")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

class HorarioDoctor(TestDoctorMixin, generic.ListView):
    template_name = "pages/horario_doctor.html"
    login_url = URL_LOGIN
    model = Hora

    def get_queryset(self):
        doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        return Hora.objects.filter(Q(Doctor=doctor)).order_by("Dia")

class BorrarHora(TestDoctorMixin, generic.DeleteView):
    template_name = "pages/borrar_hora.html"
    login_url = URL_LOGIN
    model = Hora
    success_url = reverse_lazy("Clinica:horario_doctor")

    ###_____________________________Citas___________________________________

class CitasDoctor(TestDoctorMixin, generic.ListView):#No implementado
    template_name = "pages/doctor_citas.html"
    login_url = URL_LOGIN
    model = Cita

    def get_queryset(self):
        doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        return Cita.objects.filter(Q(Doctor=doctor)).order_by("Fecha")


class VerPaciente(TestDoctorMixin, generic.DetailView):
    login_url = URL_LOGIN
    template_name = "pages/expedientepaciente.html"
    model = ExpedientePaciente
    success_url = reverse_lazy("Clinica:doctor_citas")

    ###_____________________________Notas___________________________________

class VerNotas(TestDoctorMixin, generic.ListView):
    login_url = URL_LOGIN
    template_name = "pages/lista_notas.html"
    model = Nota
    success_url = reverse_lazy("Clinica:doctor_citas")

    def get_queryset(self):
        paciente= ExpedientePaciente.objects.get(pk=self.kwargs['id'])
        return Nota.objects.filter(Q(Expedientepaciente=paciente)).order_by("FechaCreacion")


class CrearNota(TestDoctorMixin, generic.CreateView):
    login_url = URL_LOGIN
    template_name = "pages/crear_notas.html"
    model = Nota
    form_class = NotaForm
    success_url = reverse_lazy("Clinica:lista_notas")

    def form_valid(self, form):
        paciente= ExpedientePaciente.objects.get(pk=self.kwargs['id'])
        self.object = form.save(commit=False)
        self.object.Expedientepaciente = paciente
        self.object.save()

    def get_success_url(self):
          doctor=self.kwargs['pk']
          return reverse_lazy('Clinica:lista_notas', pk=self.kwargs['id'])



    ###_____________________________API___________________________________


def wsClient(request):
    url="http://localhost:8000/api/usuarios_list/"
    response = requests.get(url)
    response = response.json()
    context = {
        "object_list":response
    }
    return render(request,"base/client.html",context)
