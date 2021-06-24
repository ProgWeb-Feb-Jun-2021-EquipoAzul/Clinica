from rest_framework import serializers
from Clinica.models import Usuario

class UsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("username","TipoEmpleado","Nombres","ApellidoPaterno", "ApellidoMaterno",
         "Genero","Nacimiento","email", "Telefono", "password")

    def create(self,validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id","TipoEmpleado","Nombres","ApellidoPaterno", "ApellidoMaterno")

class UsuarioDelateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id","TipoEmpleado","Nombres","ApellidoPaterno","ApellidoMaterno",
        "Genero","Nacimiento","email","Telefono")

class UsuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id","TipoEmpleado","Nombres","ApellidoPaterno","ApellidoMaterno",
        "Genero","Nacimiento","email","Telefono","password")


    def update(self,instance,validated_data):
        update_user = super().update(instance,validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user
