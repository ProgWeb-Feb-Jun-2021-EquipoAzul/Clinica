from django.urls import path
from Clinica import views

app_name = "Clinica"

urlpatterns = [
    path('index/',views.Index.as_view(),name="index"),
    path('nuevo_usuario/',views.NuevoUsuario.as_view(), name="nuevo_usuario"),
]
