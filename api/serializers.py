from rest_framework import serializers
from Clinica.models import Usuario

class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class UsuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
