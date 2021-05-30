from django.urls import path
from Clinica import views

app_name = "Clinica"

urlpatterns = [
    #path('login/',views.Login.as_view(),name="login"),
    path('index/',views.Index.as_view(),name="index"),
    path('test/',views.Test.as_view(), name="test"),
    path('nuevo_usuario/',views.NuevoUsuario.as_view(), name="nuevo_usuario"),
]
