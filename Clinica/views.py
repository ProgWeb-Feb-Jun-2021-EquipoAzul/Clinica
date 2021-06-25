from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import HttpResponse
import requests
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora)

from .forms import (NuevoUsuarioForm, EditarUsuarioForm, ExpedientePacienteForm, NotaForm, CitaForm, DoctorForm,
HoraForms,EditarPacienteForm,CitaForm, EditarTratamientoForm, TratamientoForm, CitaForm, PerfilDoctorForm, EditarCitaForm

,FiltroUsuarios,FiltroTratamientos, FiltroPacientes, FiltroDoctores, FiltroCitas, EditarHoraForms)


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
    success_url = reverse_lazy("Clinica:lista_tratamientos")

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
    success_url = reverse_lazy("Clinica:lista_pacientes")

    ###_____________________________Citas_________________________________________
class ListaCitas(generic.ListView):
    template_name = "pages/lista_citas.html"
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
    form_class=EditarCitaForm
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

class DetallesDoctor(generic.DetailView):
    template_name = "pages/detalles_doctor.html"
    model = Doctor
    success_url = reverse_lazy("Clinica:lista_doctores")

#-----------------VIEWS DOCTOR-----------------
    ###_____________________________Perfil_________________________________________
#No implementado
class PerfilDoctor(generic.DetailView):
    template_name = "pages/perfil.html"
    model = Doctor

class EditarPerfil(generic.UpdateView):
    template_name = "pages/editar_perfil.html"
    model = Doctor
    form_class=PerfilDoctorForm

    def get_success_url(self):
          doctor=self.kwargs['pk']
          return reverse_lazy('Clinica:perfil', kwargs={'pk': doctor})

    ###_____________________________Horario___________________________________
#Mas o menos implementado solo debe de dejar entrar a doctores
class AgregarHorario(generic.CreateView):
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

class DetallesCitaDoctor(generic.DetailView):
    template_name = "pages/detalles_cita_doctor.html"
    model = Cita
    success_url = reverse_lazy("Clinica:lista_citas")

class EditarHorario(generic.UpdateView):
    template_name = "pages/editar_horario.html"
    model = Hora
    form_class=EditarHoraForms
    success_url = reverse_lazy("Clinica:horario_doctor")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.Doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        obj.save()
        return super().form_valid(form)

class HorarioDoctor(generic.ListView):
    template_name = "pages/horario_doctor.html"
    model = Hora

    def get_queryset(self):
        doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        return Hora.objects.filter(Q(Doctor=doctor)).order_by("Dia")

class BorrarHora(LoginRequiredMixin,generic.DeleteView):
    template_name = "pages/borrar_hora.html"
    login_url = URL_LOGIN
    model = Hora
    success_url = reverse_lazy("Clinica:horario_doctor")

    ###_____________________________Citas___________________________________

class CitasDoctor(generic.ListView):#No implementado
    template_name = "pages/doctor_citas.html"
    model = Cita

    def get_queryset(self):
        doctor = Doctor.objects.filter(Usuario=self.request.user).first()
        return Cita.objects.filter(Q(Doctor=doctor)).order_by("Fecha")


class VerPaciente(generic.DetailView):
    template_name = "pages/expedientepaciente.html"
    model = ExpedientePaciente
    success_url = reverse_lazy("Clinica:doctor_citas")

    ###_____________________________Notas___________________________________

class VerNotas(generic.ListView):
    template_name = "pages/lista_notas.html"
    model = Nota
    success_url = reverse_lazy("Clinica:doctor_citas")

    def get_queryset(self):
        paciente= ExpedientePaciente.objects.get(pk=self.kwargs['id'])
        return Nota.objects.filter(Q(Expedientepaciente=paciente)).order_by("FechaCreacion")


class CrearNota(generic.CreateView):
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


'''def wsClient(request):
    url="http://localhost:8000/api/usuarios_list/"
    response = requests.get(url)
    response = response.json()
    context = {
        "object_list":response
    }
    return render(request,"base/client.html",context)'''

'''def wsBoleta(request):
    data = serializers.serialize("json", Materia_Actual.objects.all())
    return HttpResponse(data, content_type="application/json")'''







def wsListaUsuarios(request):
    url = "http://localhost:8000/api/lista_usuario"
    response = requests.get(url)
    response = response.json()
    context = {
        "object_list": response
    }
    return render(request, "pages/wscliente.html",context)



def wsdetalles_usuario(request):
    url = "http://localhost:8000/api/detalles_usuario/"
    response = requests.get(url)
    response = response.json()
    context = {
        "object_list": response
    }
    return render(request, "pages/detalles_usuario.html",context)


class DetallesUsuarioAPI(generic.DetailView):
    template_name = "pages/wsdetail.html"
    model = Usuario

def wsCrearUsuario(request):
    url = "http://localhost:8000/api/crear_usuario"
    response = requests.get(url)
    response = response.json()
    context = {
        "object_list": response
    }
    return render(request, "pages/nuevo_usuario.html",context)

'''@api_view(["GET", "POST"])
def lista_usuarios(request):
    if request.method == "GET":
        usuarios = Usuario.objects.all()
        serializer = UsuarioListSerializer(usuarios, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = UsuarioListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
def detalles_usuario(request, pk=None):
    queryset = Usuario.objects.filter(id=pk).first
    if queryset:
        if request.method == "GET":
            data = UsuarioDetailSerializer(queryset)
            return Response(data.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
            data = UsuarioDetailSerializer(queryset, data = request.data)
            if data.is_valid():
                data.save()
                return Response(data.data)
            return Response(data.errors, status = status.HTTP_400_BAD_REQUEST)'''


    #elif request.method == "DELETE":

        #queryset.delete(
        #return Response({"message": "UsarioDestroy Successsfull"}, status=status.HTTP_200_OK)

  #return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
