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

                ######################################################
                #-----------------CLASES PRIVILEGIOS-----------------#
                ######################################################

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

                ###################################################
                #-----------------VIEWS GENERALES-----------------#
                ###################################################

#Vista para cuando no tenga acceso a una pagina el usuario
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

                ################################################
                #--------------VIEWS ADMINISTRADOR-------------#
                ################################################


###____________________________________Usuarios________________________________________###

#Vista de lista de usuarios
class ListaUsuarios(TestAdministradorMixin, generic.ListView):
    template_name = "pages/lista_usuarios.html"

    #Sobre escribimos el metodo del query
    def get_queryset(self):
        #Variables del form de busqueda
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        #Query de usuarios recepcionista y doctor
        usuarios = Usuario.objects.filter(~Q(TipoEmpleado = 'A'))

        #Filtros de los usuarios
        if filter_field == "all":
            return usuarios.filter(Q(Nombres__icontains=query) | Q(email__icontains=query) | Q(TipoEmpleado__icontains=query)).order_by("Nombres")
        elif filter_field == "Nombres":
            return usuarios.filter(Q(Nombres__icontains=query)).order_by("Nombres")
        elif filter_field == "email":
            return usuarios.filter(Q(email__icontains=query)).order_by("Nombres")
        elif filter_field == "TipoEmpleado":
            return usuarios.filter(Q(TipoEmpleado__icontains=query)).order_by("Nombres")
        else:
            return usuarios

    #Metodo para sacar los datos del form de busqueda
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroUsuarios(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        return context

#Vista de creacion de un usuario
class NuevoUsuario(TestAdministradorMixin, TestRecepcionistaMixin,generic.CreateView):
    template_name = "pages/nuevo_usuario.html"
    model = Usuario
    form_class = NuevoUsuarioForm
    success_url = reverse_lazy("Clinica:lista_usuarios")

#Vista para editar un usuario
class EditarUsuario(TestAdministradorMixin, generic.UpdateView):
    template_name = "pages/editar_usuario.html"
    model = Usuario
    form_class = EditarUsuarioForm
    success_url = reverse_lazy("Clinica:lista_usuarios")

#Vista para cambiar la contraseña de un usuario
class CambiarContrasenaUsuario(TestAdministradorMixin, generic.UpdateView):
    template_name = "pages/editar_contrasena.html"
    model = Usuario
    form_class = ContrasenaUsuarioForm
    success_url = reverse_lazy("Clinica:lista_usuarios")

#Vista para ver los detalles de un usuario
class DetallesUsuario(TestAdministradorMixin, generic.DetailView):
    template_name = "pages/detalles_usuario.html"
    model = Usuario

#Vista para cambiar borrar un usuario
class BorrarUsuario(TestAdministradorMixin, generic.DeleteView):
    template_name = "pages/borrar_usuario.html"
    model = Usuario
    success_url = reverse_lazy("Clinica:lista_usuarios")

###____________________________________Tratamientos________________________________________###

#Vista para la lista de tratamientos
class ListaTratamiento(TestAdministradorMixin, generic.ListView):
    template_name = "pages/lista_tratamientos.html"
    model =  Tratamiento

    #Sobre escribimos el metodo del query
    def get_queryset(self):
        #Variable del form de busqueda
        query = self.request.GET.get('search')

        #Filtros de los tratamientos
        if not query:
            return Tratamiento.objects.all().order_by("Tratamiento")
        else:
            return Tratamiento.objects.filter(Q(Tratamiento__icontains=query)).order_by("Tratamiento")

    #Metodo para sacar los datos del form de busqueda
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroTratamientos(initial={
            'search': self.request.GET.get('search', ''),
        })

        return context

#Vista para crear un tratamiento
class CrearTratamiento(TestAdministradorMixin, generic.CreateView):
    template_name = "pages/crear_tratamiento.html"
    model = Tratamiento
    form_class = TratamientoForm
    success_url = reverse_lazy("Clinica:lista_tratamientos")

#Vista para editar un tratamiento
class EditarTratamiento(TestAdministradorMixin, generic.UpdateView):
    template_name = "pages/editar_tratamiento.html"
    model = Tratamiento
    form_class = EditarTratamientoForm
    success_url = reverse_lazy("Clinica:lista_tratamientos")

#Vista para borrar un tratamiento
class borrar_tratamiento(TestAdministradorMixin, generic.DeleteView):
    template_name = "pages/borrar_tratamiento.html"
    model = Tratamiento
    success_url = reverse_lazy("Clinica:lista_tratamientos")

                ################################################
                #--------------VIEWS RECEPCIONISTA-------------#
                ################################################

###____________________________________Pacientes____________________________________###


class ListaPacientes(TestRecepcionistaMixin, generic.ListView):
    template_name = "pages/lista_pacientes.html"
    model =  ExpedientePaciente

    #Sobre escribimos el metodo de get_query
    def get_queryset(self):
        #Variables del form de busqueda
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        #Filtros de pacientes
        if filter_field == "all":
            return ExpedientePaciente.objects.filter( Q(Nombres__icontains=query) | Q(email__icontains=query) | Q(Telefono__icontains=query)).order_by("Nombres")
        elif filter_field == "Nombres":
            return ExpedientePaciente.objects.filter(Q(Nombres__icontains=query) ).order_by("Nombres")
        elif filter_field == "email":
            return ExpedientePaciente.objects.filter(Q(Correo__icontains=query)).order_by("Nombres")
        elif filter_field == "Telefono":
            return ExpedientePaciente.objects.filter(Q(Telefono__icontains=query)).order_by("Nombres")
        else:
            return ExpedientePaciente.objects.all().order_by("Nombres")

    #Metodo para sacar los datos del form de busqueda
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroPacientes(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        return context

#Vista para crear un paciente
class CrearPaciente(TestRecepcionistaMixin, generic.CreateView):
    template_name = "pages/crear_paciente.html"
    model = ExpedientePaciente
    form_class = ExpedientePacienteForm
    success_url = reverse_lazy("Clinica:lista_pacientes")

#Vista para ver los detalles de un paciente
class DetallesPaciente(TestRecepcionistaMixin, generic.DetailView):
    template_name = "pages/detalles_paciente.html"
    model =  ExpedientePaciente
    success_url = reverse_lazy("Clinica:lista_pacientes")

#Vista para editar un paciente
class EditarPaciente(TestRecepcionistaMixin, generic.UpdateView):
    template_name =  "pages/editar_paciente.html"
    model = ExpedientePaciente
    form_class = EditarPacienteForm
    success_url = reverse_lazy("Clinica:lista_pacientes")

###_____________________________Citas_________________________________________###

#Vista de lista de citas
class ListaCitas(TestRecepcionistaMixin, generic.ListView):
    template_name = "pages/lista_citas.html"
    model = Cita

    #Sobre escribimos el metodo del query
    def get_queryset(self):
        #Variables del form de busqueda
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        #Filtros de citas
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

    #Metodo para sacar los datos del form de busqueda
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroCitas(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        return context

#Vista para crear una cita
class CrearCita(TestRecepcionistaMixin, generic.CreateView):
    template_name = "pages/crear_cita.html"
    model =  Cita
    form_class = CitaForm
    success_url = reverse_lazy("Clinica:lista_citas")

#Vista para ver los detalles de una cita
class DetallesCita(TestRecepcionistaMixin, generic.DetailView):
    template_name = "pages/detalles_cita.html"
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

#Vista para editar una cita
class EditarCita(TestRecepcionistaMixin, generic.UpdateView):
    template_name = "pages/editar_cita.html"
    model = Cita
    form_class=EditarCitaForm
    success_url = reverse_lazy("Clinica:lista_citas")

#Vista para borrar una cita
class BorrarCita(TestRecepcionistaMixin, generic.DeleteView): ###Falta completar
    template_name = "pages/borrar_cita.html"
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

###_____________________________Doctores_________________________________________###

#Vista de la lista de doctores
class ListaDoctores(TestRecepcionistaMixin, generic.ListView):
    template_name = "pages/lista_doctores.html"
    model = Doctor

    #Sobre escribimos el metodo del query
    def get_queryset(self):
        #Variables del form de busqueda
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        #Filtro para doctores
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

    #Metodo para sacar los datos del form de busqueda
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FiltroDoctores(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        return context

#Vista para ver los detalles del doctor
class DetallesDoctor(TestRecepcionistaMixin, generic.DetailView):
    template_name = "pages/detalles_doctor.html"
    model = Doctor
    success_url = reverse_lazy("Clinica:lista_doctores")

                    ################################################
                    #-----------------VIEWS DOCTOR-----------------#
                    ################################################

###_____________________________Perfil_________________________________________###

#Vista para ver el perfil del doctor
class PerfilDoctor(TestDoctorMixin, generic.DetailView):
    template_name = "pages/perfil.html"
    model = Doctor

#Vista para editar los tratamientos
class EditarPerfil(TestDoctorMixin, generic.UpdateView):
    template_name = "pages/editar_perfil.html"
    model = Doctor
    form_class=PerfilDoctorForm

    #Sobrescribimos get_success_url para devolvernos al perfil correcto
    def get_success_url(self):
          doctor=self.kwargs['pk']
          return reverse_lazy('Clinica:perfil', kwargs={'pk': doctor})

###_____________________________Horario___________________________________###


#Vista para agregar una hora
class AgregarHorario(TestDoctorMixin, generic.CreateView):
    template_name = "pages/agregar_horario.html"
    model = Hora
    form_class = HoraForms
    success_url = reverse_lazy("Clinica:horario")

    #Agrega la pk de doctor a la que pertenece la hora agregada
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

#Vista para ver los detalles de la cita
class DetallesCitaDoctor(TestDoctorMixin, generic.DetailView):
    template_name = "pages/detalles_cita_doctor.html"
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

#Vista para editar el horario
class EditarHorario(TestDoctorMixin, generic.UpdateView):
    template_name = "pages/editar_horario.html"
    model = Hora
    form_class=EditarHoraForms
    success_url = reverse_lazy("Clinica:horario")

    #Si es valida la informaicon para no mostrar a que doctor se modifica se hace un query
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

#Vista de las horas del doctor
class HorarioDoctor(TestDoctorMixin, generic.ListView):
    template_name = "pages/horario_doctor.html"
    model = Hora

    #Sobreescribimos el medoto del get_query para solo sacar las horas del doctor
    def get_queryset(self):
        doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        return Hora.objects.filter(Q(Doctor=doctor)).order_by("Dia")

#Vista para borrar una hora
class BorrarHora(TestDoctorMixin, generic.DeleteView):
    template_name = "pages/borrar_hora.html"
    model = Hora
    success_url = reverse_lazy("Clinica:horario")

###_____________________________Citas___________________________________###

#Vista de las citas del doctor
class CitasDoctor(TestDoctorMixin, generic.ListView):#No implementado
    template_name = "pages/doctor_citas.html"
    model = Cita

    def get_queryset(self):
        doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        return Cita.objects.filter(Q(Doctor=doctor)).order_by("Fecha")

#Vista para ver el paciente de la cita
class VerPaciente(TestDoctorMixin, generic.DetailView):
    template_name = "pages/expedientepaciente.html"
    model = ExpedientePaciente
    success_url = reverse_lazy("Clinica:doctor_citas")

###_____________________________Notas___________________________________###

#Vista para ver las notas del paciente
class VerNotas(TestDoctorMixin, generic.ListView):
    template_name = "pages/lista_notas.html"
    model = Nota
    success_url = reverse_lazy("Clinica:doctor_citas")

    #Sobre escribimos el metodo get_query para solo cargar las notas del paciente
    def get_queryset(self):
        paciente= ExpedientePaciente.objects.get(pk=self.kwargs['id'])
        return Nota.objects.filter(Q(Expedientepaciente=paciente)).order_by("FechaCreacion")

#Vista para crear notas al paciente
class CrearNota(TestDoctorMixin, generic.CreateView):
    template_name = "pages/crear_notas.html"
    model = Nota
    form_class = NotaForm

    #Si la informacion es validad le ingresamos automaticamente al paciente a que va la nota
    def form_valid(self, form):
        paciente= ExpedientePaciente.objects.get(pk=self.kwargs['id'])
        self.object = form.save(commit=False)
        self.object.Expedientepaciente = paciente
        self.object.save()
        return super().form_valid(form)

    #Redireccionamos a la lista de citas
    def get_success_url(self):
          #return reverse_lazy('Clinica:ver_notas', kwargs=self.kwargs['id'])
          return reverse_lazy('Clinica:doctor_citas')

###_____________________________APIs___________________________________###

def wsClient(request):
    url="http://localhost:8000/api/usuarios_list/"
    response = requests.get(url)
    response = response.json()
    context = {
        "object_list":response
    }
    return render(request,"base/client.html",context)
