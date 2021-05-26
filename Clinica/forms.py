from django import forms
from django.core.validators import RegexValidator

from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora,
Doctor_Hora)

TIPO_EMPLEADO = (
        ('A', 'Administrador'),
        ('R', 'Recepcionista'),
        ('D', 'Doctor'),
    )

GENERO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

class UsuarioForm(forms.ModelForm):
    NombreUsuario = forms.CharField(
        max_length=30,
        label="Cuenta del usuario",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Jesus10", "class": "form-control"})
        )
    Contrasena = forms.CharField(
        max_length=50,
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "*********", "class": "form-control"})
        )
    TipoEmpleado = forms.ChoiceField(
        choices = TIPO_EMPLEADO,
        label="Tipo de empleado",
        required=True)
    Nombres = forms.CharField(
        max_length=50,
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Jesús Manuel", "class": "form-control"})
        )
    ApellidoPaterno = forms.CharField(
        max_length=50,
        label="Apellido Paterno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Cota", "class": "form-control"}))
    ApellidoMaterno = forms.CharField(
        max_length=50,
        label="Apellido Materno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Villa", "class": "form-control"}))
    Genero = forms.ChoiceField(
        choices = GENERO,
        label="Género",
        required=True)
    Nacimiento = forms.DateField(
        required=True,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'}))
    Correo = forms.EmailField(
        max_length=50,
        label="Correo electrónico",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "correo@sitio.com", "class": "form-control"}))
    Telefono = forms.CharField(
        max_length=12,
        label="Telefono",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "6642545896", "class": "form-control"})
        )
    class Meta:
        model = Usuario
        fields = "__all__"
        exclude = ["UltimoAcceso"]

class ExpedientePacienteForm(forms.ModelForm):
    Nombres = forms.CharField(
        max_length=50,
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Jesús Manuel", "class": "form-control"})
        )
    ApellidoPaterno = forms.CharField(
        max_length=50,
        label="Apellido Paterno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Cota", "class": "form-control"}))
    ApellidoMaterno = forms.CharField(
        max_length=50,
        label="Apellido Materno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Villa", "class": "form-control"}))
    Genero = forms.ChoiceField(
        choices = GENERO,
        label="Género",
        required=True)
    Nacimiento = forms.DateField(
        required=True,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'}))
    Direccion = forms.CharField(
        max_length=80,
        label="Dirección",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Avenida San Juan", "class": "form-control"}))
    Correo = forms.EmailField(
        max_length=50,
        label="Correo electrónico",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "correo@sitio.com", "class": "form-control"}))
    Telefono = forms.CharField(
        max_length=12,
        label="Telefono",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "6642545896", "class": "form-control"})
        )
    Alergias = forms.CharField(
        max_length=200,
        label="Alergias",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "6642545896", "class": "form-control"})
        )
    Padecimientos = forms.CharField(
        max_length=200,
        label="Padecimientos",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "6642545896", "class": "form-control"})
        )
    class Meta:
        model = ExpedientePaciente
        fields = "__all__"
        exclude = ["FechaCreacion"]

class NotaForm(forms.ModelForm):
    Expedientepaciente = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Paciente",
        required=True,
        )
    Nota = forms.CharField(
        max_length=200,
        label="Contenido de la nota del paciente",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Nota sobre el paciente", "class": "form-control"})
        )
    class Meta:
        model = Nota
        fields = "__all__"
        exclude = ["FechaCreacion"]
