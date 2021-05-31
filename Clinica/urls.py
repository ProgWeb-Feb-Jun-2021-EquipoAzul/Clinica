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
    #Recepcionista
    #Doctor
    path('agregar_horario/',views.AgregarHorario.as_view(), name="agregar_horario"),
]
