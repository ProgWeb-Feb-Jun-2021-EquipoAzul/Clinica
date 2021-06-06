from django.urls import path
from Clinica import views

app_name = "Clinica"

urlpatterns = [
    path('index/',views.Index.as_view(),name="index"),

    #Administrador
    path('lista_usuarios/',views.ListaUsuarios.as_view(), name="lista_usuarios"),
    path('nuevo_usuario/',views.NuevoUsuario.as_view(), name="nuevo_usuario"),
    path('editar_usuario/<int:pk>', views.EditarUsuario.as_view(), name="editar_usuario"),
    path('detalles_usuario/<int:pk>', views.DetallesUsuario.as_view(), name="detalles_usuario"),
    path('borrar_usuario/<int:pk>', views.BorrarUsuario.as_view(), name="borrar_usuario"),
    ###____________________________________Tratamientos________________________________________''
    path('lista_tratamientos/', views.ListaTratamiento.as_view(), name="lista_tratamientos"),
    path('editar_tratamiento/<int:pk>', views.EditarTratamiento.as_view(), name="editar_tratamiento"),
    path('borrar_tratamiento/<int:pk>', views.borrar_tratamiento.as_view(), name="borrar_tratamiento"),
    path('crear_tratamiento/', views.CrearTratamiento.as_view(), name="crear_tratamiento"),
    #Recepcionista
    path('lista_pacientes/', views.ListaPacientes.as_view(), name="lista_pacientes"),
    path('editar_paciente/<int:pk>/', views.EditarPaciente.as_view(), name="editar_paciente"),
    path('detalles_paciente/<int:pk>/', views.DetallesPaciente.as_view(), name="detalles_paciente"),
    ###_____________________________Citas_________________________________________
    path('crear_cita/', views.CrearCita.as_view(), name="crear_cita"),
    path('lista_citas/', views.ListaCitas.as_view(), name="lista_citas"),
    path('editar_cita/<int:pk>', views.EditarCita.as_view(), name="editar_cita"),
    path('borrar_cita/<int:pk>', views.BorrarCita.as_view(), name="borrar_cita"),
    path('detalles_cita/<int:pk>/', views.DetallesCita.as_view(), name="detalles_cita"),
    #Doctor
    path('lista_doctores/', views.ListaDoctores.as_view(), name="lista_doctores"),
    path('detalles_doctor/<int:pk>/', views.DetallesDoctor.as_view(), name="detalles_doctor"),

    #path('agregar_horario/',views.AgregarHorario.as_view(), name="agregar_horario"),
    #path('lista_usuarios/', views.ListaUsuarios.as_view(), name="lista_usuarios"),

    #path('crear_tratamiento/', views.CrearTratamiento.as_view(), name="crear_tratamiento"),





    #path('doctor/<int:pk>/', views.PerfilDoctor.as_view(), name="doctor"),
    #path('doctor_tratamientos/', view.TramientosDoctor.as_view(), name="doctor_tratamientos"),
    #path('horario_doctor/', views.HorarioDoctor.as_view(), name="horario_doctor"),
    #path('editar_horario/<int:pk>/', views.EditarHorario.as_view(), name='editar_horario'),
    #path('doctor_citas/', views.CitasDoctor.as_view(), name="doctor_citas"),
    #path('doctor_notas', views.VerNotas.as_view(), name="doctor_notas"),
    #path('crear_notas', views.CrearNota.as_view(), name="crear_notas"),
    #path('expedientepaciente/<int:pk>/', views.VerPaciente.as_view(), name="expedientepaciente")
]
