from rest_framework import serializers

from Clinica.models import Usuario

class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id","TipoEmpleado","Nombres","ApellidoPaterno", "ApellidoMaterno",
         "Genero","Nacimiento","email", "Telefono")

class UsuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id","TipoEmpleado","Nombres","ApellidoPaterno","ApellidoMaterno",
        "Genero","Nacimiento","email","Telefono")
