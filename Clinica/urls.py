from django.urls import path
from Clinica import views

app_name = "Clinica"

urlpatterns = [
    path('index/',views.Index.as_view(),name="index"),

    #Administrador

        ###____________________________________Usuarios________________________________________''
    path('lista_usuarios/',views.ListaUsuarios.as_view(), name="lista_usuarios"), #Para decorar
    path('nuevo_usuario/',views.NuevoUsuario.as_view(), name="nuevo_usuario"), #Para decorar
    path('editar_usuario/<int:pk>', views.EditarUsuario.as_view(), name="editar_usuario"), #Para decorar
    path('detalles_usuario/<int:pk>', views.DetallesUsuario.as_view(), name="detalles_usuario"), #Para decorar
    path('borrar_usuario/<int:pk>', views.BorrarUsuario.as_view(), name="borrar_usuario"), #Para decorar

        ###____________________________________Tratamientos____________________________________''
    path('lista_tratamientos/', views.ListaTratamiento.as_view(), name="lista_tratamientos"), #Para decorar
    path('editar_tratamiento/<int:pk>', views.EditarTratamiento.as_view(), name="editar_tratamiento"), #Para decorar
    path('borrar_tratamiento/<int:pk>', views.borrar_tratamiento.as_view(), name="borrar_tratamiento"), #Para decorar
    path('crear_tratamiento/', views.CrearTratamiento.as_view(), name="crear_tratamiento"), #Para decorar

    #Recepcionista

        ###____________________________________Pacientes____________________________________''
    path('lista_pacientes/', views.ListaPacientes.as_view(), name="lista_pacientes"),#Para decorar
    path('editar_paciente/<int:pk>/', views.EditarPaciente.as_view(), name="editar_paciente"),#Para decorar
    path('detalles_paciente/<int:pk>/', views.DetallesPaciente.as_view(), name="detalles_paciente"),#Para decorar
    path('crear_paciente/', views.CrearPaciente.as_view(), name="crear_paciente"),#Para decorar
        ###_____________________________Citas_________________________________________
    path('crear_cita/', views.CrearCita.as_view(), name="crear_cita"),#De lista citas y del menu (Incompleto)
    #Falta crear citas desde pacientes
    path('lista_citas/', views.ListaCitas.as_view(), name="lista_citas"),
    path('editar_cita/<int:pk>', views.EditarCita.as_view(), name="editar_cita"),
    path('borrar_cita/<int:pk>', views.BorrarCita.as_view(), name="borrar_cita"),
    path('detalles_cita/<int:pk>/', views.DetallesCita.as_view(), name="detalles_cita"),

        ###_____________________________Doctores_________________________________________
    path('lista_doctores/', views.ListaDoctores.as_view(), name="lista_doctores"), #Para decorar
    path('detalles_doctor/<int:pk>/', views.DetallesDoctor.as_view(), name="detalles_doctor"), #Para decorar

    #Doctor

        ###_____________________________Perfil_________________________________________
    path('perfil/<int:pk>/', views.PerfilDoctor.as_view(), name="perfil"), #Para decorar
    path('editar_perfil/<int:pk>/', views.EditarPerfil.as_view(), name="editar_perfil"), #Para decorar

        ###_____________________________Horario___________________________________
    path('horario/', views.HorarioDoctor.as_view(), name="horario"), #Para decorar #Falta barra de busqueda
    path('crear_horario/',views.AgregarHorario.as_view(), name="crear_horario"), #Para decorar
    path('editar_horario/<int:pk>/', views.EditarHorario.as_view(), name='editar_horario'), #Para decorar
    path('borrar_horario/<int:pk>/', views.BorrarHora.as_view(), name='borrar_horario'), #Para decorar

        ###_____________________________Citas___________________________________
    #path('doctor_citas/', views.CitasDoctor.as_view(), name="doctor_citas"), #No implementado #Citas del doctor
    #path('expedientepaciente/<int:pk>/', views.VerPaciente.as_view(), name="expedientepaciente") #No implementado #Expediente de la cita del doc

        ###_____________________________Pacientes___________________________________


        ###_____________________________Notas___________________________________
    #path('doctor_notas', views.VerNotas.as_view(), name="doctor_notas"), #No implementado #Ver notas del paciente
    #path('crear_notas', views.CrearNota.as_view(), name="crear_notas"), #No implementado #Crear nota al paciente

]

#quitar la barra superior
