from django import forms
from django.core.validators import RegexValidator

from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora)


TIPO_EMPLEADO = (
        ('A', 'Administrador'),
        ('R', 'Recepcionista'),
        ('D', 'Doctor'),
    )

GENERO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

DIAS = (
        ('Domingo', 'Domingo'),
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miercoles', 'Miercoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sabado', 'Sabado'),
    )
HORAS = (
        ('00:00', '00:00 am'),('01:00', '01:00 am'),('02:00', '02:00 am'),('03:00', '03:00 am'),
        ('04:00', '04:00 am'),('05:00', '05:00 am'),('06:00', '06:00 am'),('07:00', '07:00 am'),
        ('08:00', '08:00 am'),('09:00', '09:00 am'),('10:00', '10:00 am'),('11:00', '11:00 am'),
        ('12:00', '12:00 pm'),('13:00', '01:00 pm'),('14:00', '02:00 pm'),('15:00', '03:00 pm'),
        ('16:00', '04:00 pm'),('17:00', '05:00 pm'),('18:00', '06:00 pm'),('19:00', '07:00 pm'),
        ('20:00', '08:00 pm'),('21:00', '09:00 pm'),('22:00', '10:00 pm'),('23:00', '11:00 pm'),
    )

class NuevoUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
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
        widget=forms.DateInput(format='%d/%m/%Y',attrs={'type': 'date'}))
    email = forms.EmailField(
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
        fields = 'username', 'password1', 'password2', 'TipoEmpleado','Nombres','ApellidoPaterno','ApellidoMaterno','Genero','Nacimiento','email','Telefono'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        Usuario = super(UsuarioForm, self).save(commit=False)
        Usuario.set_password(self.cleaned_data["password1"])
        if commit:
            Usuario.save()
        return Usuario

class EditarUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
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
        widget=forms.DateInput(format='%d/%m/%Y',attrs={'type': 'date'}))
    email = forms.EmailField(
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
        fields = 'username', 'password1', 'password2', 'TipoEmpleado','Nombres','ApellidoPaterno','ApellidoMaterno','Genero','Nacimiento','email','Telefono'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        Usuario = super(UsuarioForm, self).save(commit=False)
        Usuario.set_password(self.cleaned_data["password1"])
        if commit:
            Usuario.save()
        return Usuario

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
        widget=forms.DateInput(format='%d/%m/%Y',attrs={'type': 'date'}))
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
        widget=forms.Textarea(attrs={"placeholder": "Descripción de las alergias del paciente.", "class": "form-control"})
        )
    Padecimientos = forms.CharField(
        max_length=200,
        label="Padecimientos",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Descripción de Padecimientos del paciente.", "class": "form-control"})
        )
    class Meta:
        model = ExpedientePaciente
        fields = "__all__"
        exclude = ["FechaCreacion"]

class EditarPacienteForm(forms.ModelForm):
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
        widget=forms.DateInput(format='%d/%m/%Y',attrs={'type': 'date'}))
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
        widget=forms.Textarea(attrs={"placeholder": "Descripción de las alergias del paciente.", "class": "form-control"})
        )
    Padecimientos = forms.CharField(
        max_length=200,
        label="Padecimientos",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Descripción de Padecimientos del paciente.", "class": "form-control"})
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
        widget=forms.Textarea(attrs={"placeholder": "Nota sobre el paciente.", "class": "form-control"})
        )
    class Meta:
        model = Nota
        fields = "__all__"
        exclude = ["FechaCreacion"]

class TratamientoForm(forms.ModelForm):
    Tratamiento = forms.CharField(
        max_length=50,
        label="Nombre del tratamiento",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Tratamiento", "class": "form-control"})
        )
    Descripcion = forms.CharField(
        max_length=200,
        label="Descripción del tratamiento",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Aqui esta la explicacion del tratamiento.", "class":"form-control"})
        )
    class Meta:
        model = Tratamiento
        fields = "__all__"
        exclude = []

class EditarTratamientoForm(forms.ModelForm):
    Tratamiento = forms.CharField(
        max_length=50,
        label="Nombre del tratamiento",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Tratamiento", "class": "form-control"})
        )
    Descripcion = forms.CharField(
        max_length=200,
        label="Descripción del tratamiento",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Aqui esta la explicacion del tratamiento.", "class":"form-control"})
        )
    class Meta:
        model = Tratamiento
        fields = "__all__"
        exclude = []

'''
Los tratamientos se llenarian con una tabla
'''
class DoctorForm(forms.ModelForm):
    Usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Empleado",
        required=True,
        )
    class Meta:
        model = Doctor
        fields = "__all__"
        exclude = []

'''
Buscar como hacer eventos para hacer los queries de las horas y
tratamientos del Doctor cuando se selecciona el doctor
'''
class CitaForm(forms.ModelForm):
    Doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        label="Doctor",
        required=True)
    ExpedientePaciente = forms.ModelChoiceField(
        queryset=ExpedientePaciente.objects.all(),
        label="Paciente",
        required=True)
    Fecha = forms.DateField(
        required=True,
        label="Fecha de la cita",
        widget=forms.DateInput(format='%d/%m/%Y',attrs={'type': 'date'}))
    HoraInicio=forms.TimeField(
        required=True,
        label="Hora inicio de la cita",
        widget=forms.TimeInput(format='%H:%M'))
    HoraFin=forms.TimeField(
        required=True,
        label="Hora fin de la cita",
        widget=forms.TimeInput(format='%H:%M'))
    Tratamiento = forms.CharField(
        max_length=50,
        label="Tratamiento a realizarse",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Tratamiento", "class": "form-control"}))

    class Meta:
        model = Cita
        fields = "__all__"
        exclude = ["FechaCreacion"]

class HoraForms(forms.ModelForm):
    Dia = forms.ChoiceField(
        choices = DIAS,
        label="Dia",
        required=True)
    Hora = forms.ChoiceField(
        choices = HORAS,
        label="Hora",
        required=True)

    class Meta:
        model = Hora
        fields = 'Dia','Hora'
        exclude = []
