from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Clinica.models import Usuario
from .serializers import UsuarioListSerializer, UsuarioDetailSerializer

# Create your views here.

class UsuarioList(APIView):
    def get(self, request):
        personas = Usuario.objects.all()
        data = UsuarioListSerializer(personas, many=True).data
        return Response(data)

class UsuarioDetail(APIView):
    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        data = UsuarioDetailSerializer(usuario).data
        return Response(data)
