from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,

    )
from django.http import Http404
from Clinica.models import Usuario
from .serializers import UsuarioListSerializer, UsuarioDetailSerializer, UsuarioCreateSerializer,UsuarioDelateSerializer

# Create your views here.
class UsuarioCreateSet(CreateAPIView):
        #def get(self, request, format=None):
        queryset = Usuario.objects.all()
        serializer_class = UsuarioCreateSerializer
        lookup_field = "sulgi"



class UsuarioListSet(ListAPIView):
        #def get(self, request, format=None):
        queryset = Usuario.objects.all()
        serializer_class = UsuarioListSerializer
        lookup_field = "sulgi"
        #return Response(serializer.data)

class UsuarioUpdateSet(RetrieveUpdateAPIView):
        queryset = Usuario.objects.all()
        serializer_class = UsuarioDetailSerializer

    #def perform_update(self, serializer):
        #serializer.save(user=self.request.user


class UsuarioDetailSet(RetrieveAPIView):
    def get(seft, request, *args, **kwargs):
        user = get_object_or_404(Usuario, pk=kwargs['pk'])
        serializer_class = UsuarioDelateSerializer(user).data
        return Response(serializer_class)


class UsuarioDeleteSet(RetrieveDestroyAPIView):
        queryset = Usuario.objects.all()
        serializer_class = UsuarioDelateSerializer
