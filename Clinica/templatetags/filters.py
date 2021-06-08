from django import template

from Clinica.models import (Usuario, Doctor)

register = template.Library()

@register.filter(name ='pk_doctor')
def pk_doctor(pkUsuario):
    return Doctor.objects.filter(Usuario=pkUsuario).first().id
