from django.urls import path
from Clinica import views

app_name = "Clinica"

urlpatterns = [


    path('redirect/',views.Redirect.as_view(),name="redirect"),
    path('login/',views.LoginView.as_view(),name="login"),

    #######################################
    #------------Administrador------------#
    #######################################

        ###____________________________________Usuarios________________________________________###
    path('lista_usuarios/',views.ListaUsuarios.as_view(), name="lista_usuarios"),
    path('nuevo_usuario/',views.NuevoUsuario.as_view(), name="nuevo_usuario"),
    path('editar_usuario/<int:pk>', views.EditarUsuario.as_view(), name="editar_usuario"),
    path('detalles_usuario/<int:pk>', views.DetallesUsuario.as_view(), name="detalles_usuario"),
    path('borrar_usuario/<int:pk>', views.BorrarUsuario.as_view(), name="borrar_usuario"),
    path('cambiar_contrasena/<int:pk>', views.CambiarContrasenaUsuario.as_view(), name="cambiar_contrasena"),

        ###____________________________________Tratamientos____________________________________###
    path('lista_tratamientos/', views.ListaTratamiento.as_view(), name="lista_tratamientos"),
    path('editar_tratamiento/<int:pk>', views.EditarTratamiento.as_view(), name="editar_tratamiento"),
    path('borrar_tratamiento/<int:pk>', views.borrar_tratamiento.as_view(), name="borrar_tratamiento"),
    path('crear_tratamiento/', views.CrearTratamiento.as_view(), name="crear_tratamiento"),

    #######################################
    #------------Recepcionista------------#
    #######################################

        ###____________________________________Pacientes____________________________________###
    path('lista_pacientes/', views.ListaPacientes.as_view(), name="lista_pacientes"),
    path('editar_paciente/<int:pk>/', views.EditarPaciente.as_view(), name="editar_paciente"),
    path('detalles_paciente/<int:pk>/', views.DetallesPaciente.as_view(), name="detalles_paciente"),
    path('crear_paciente/', views.CrearPaciente.as_view(), name="crear_paciente"),

        ###_____________________________Citas_________________________________________###
    path('crear_cita/', views.CrearCita.as_view(), name="crear_cita"),
    path('lista_citas/', views.ListaCitas.as_view(), name="lista_citas"),
    path('editar_cita/<int:pk>', views.EditarCita.as_view(), name="editar_cita"),
    path('borrar_cita/<int:pk>', views.BorrarCita.as_view(), name="borrar_cita"),
    path('detalles_cita/<int:pk>/', views.DetallesCita.as_view(), name="detalles_cita"),

        ###_____________________________Doctores_________________________________________###
    path('lista_doctores/', views.ListaDoctores.as_view(), name="lista_doctores"),
    path('detalles_doctor/<int:pk>/', views.DetallesDoctor.as_view(), name="detalles_doctor"),

    #######################################
    #---------------Doctor----------------#
    #######################################

        ###_____________________________Perfil_________________________________________###
    path('perfil/<int:pk>/', views.PerfilDoctor.as_view(), name="perfil"),
    path('editar_perfil/<int:pk>/', views.EditarPerfil.as_view(), name="editar_perfil"),

        ###_____________________________Horario___________________________________
    path('horario/', views.HorarioDoctor.as_view(), name="horario"),
    path('crear_horario/',views.AgregarHorario.as_view(), name="crear_horario"),
    path('editar_horario/<int:pk>/', views.EditarHorario.as_view(), name='editar_horario'),
    path('borrar_horario/<int:pk>/', views.BorrarHora.as_view(), name='borrar_horario'),

        ###_____________________________Citas___________________________________###
    path('doctor_citas/', views.CitasDoctor.as_view(), name="doctor_citas"),
    path('detalles_cita_doctor/<int:pk>/', views.DetallesCitaDoctor.as_view(), name="detalles_cita_doctor"),
    path('expedientepaciente/<int:pk>/', views.VerPaciente.as_view(), name="expedientepaciente"),

        ###_____________________________Notas___________________________________
    path('ver_notas/<int:id>', views.VerNotas.as_view(), name="ver_notas"),
    path('crear_notas/<int:id>', views.CrearNota.as_view(), name="crear_notas"),

        ###_____________________________API___________________________________
    #path('ws/client', views.wsClient, name="wsClient"),
    path('ws/cliente/lista_usuarios', views.wsListaUsuarios, name="wslista_usuarios"),
    #path('ws/cliente/detalles_usuario/<int:pk>/', views.wsdetalles_usuario.as_view(), name="wsdetalles_usuario"),
    path('ws/cliente/crear_usuario', views.wsCrearUsuario, name="wscrear_usuario"),
    #path('ws/cliente/eliminar_usuario/<int:pk>/', views.wsElminarUsuario, name="wseliminar_usuario"),
    #path('ws/cliente/editar_usuario/<int:pk>/', views.wsEditarsUsuario, name="wseditar_usuario"),

]
