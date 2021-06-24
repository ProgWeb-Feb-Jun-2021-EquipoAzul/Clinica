from django import forms
from django.core.validators import RegexValidator
from django.forms import Form

from datetime import date

from .models import (Usuario, ExpedientePaciente, Doctor,
Nota, Cita, Tratamiento, Doctor_Tratamiento, Hora)


TIPO_EMPLEADO = (
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
        ('00:00:00', '00:00 am'),('01:00:00', '01:00 am'),('02:00:00', '02:00 am'),('03:00:00', '03:00 am'),
        ('04:00:00', '04:00 am'),('05:00:00', '05:00 am'),('06:00:00', '06:00 am'),('07:00:00', '07:00 am'),
        ('08:00:00', '08:00 am'),('09:00:00', '09:00 am'),('10:00:00', '10:00 am'),('11:00:00', '11:00 am'),
        ('12:00:00', '12:00 pm'),('13:00:00', '01:00 pm'),('14:00:00', '02:00 pm'),('15:00:00', '03:00 pm'),
        ('16:00:00', '04:00 pm'),('17:00:00', '05:00 pm'),('18:00:00', '06:00 pm'),('19:00:00', '07:00 pm'),
        ('20:00:00', '08:00 pm'),('21:00:00', '09:00 pm'),('22:00:00', '10:00 pm'),('23:00:00', '11:00 pm'),
    )

class FiltroUsuarios(Form):
    FILTER_CHOICES = (
        ("all", 'Todo los campos'),
        ("Nombres", 'Nombres'),
        ("email", 'Correo'),
        ("TipoEmpleado", 'Tipo de empleado'),
    )
    search = forms.CharField(required=False)
    filter_field = forms.ChoiceField(choices=FILTER_CHOICES)

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
        widget=forms.TextInput(attrs={"placeholder": "Nombre(s)", "class": "form-control"})
        )
    ApellidoPaterno = forms.CharField(
        max_length=50,
        label="Apellido Paterno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Apellido Paterno", "class": "form-control"}))
    ApellidoMaterno = forms.CharField(
        max_length=50,
        label="Apellido Materno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Apellido Materno", "class": "form-control"}))
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
        widget=forms.TextInput(attrs={"placeholder": "Teléfono", "class": "form-control"})
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
        Usuario = super(NuevoUsuarioForm, self).save(commit=False)
        Usuario.set_password(self.cleaned_data["password1"])
        if commit:
            Usuario.save()
        return Usuario

class EditarUsuarioForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        label="username",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Usuario...", "class": "form-control-sm", "style": "border: 1px solid #dee2e6; border-width: 1px; margin-bottom: 10px;", "aria-controls": "datatable"})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña...", "class": "form-control-sm", "style": "border: 1px solid #dee2e6; border-width: 1px; margin-bottom: 10px;", "aria-controls": "datatable"})
        )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña...", "class": "form-control-sm", "style": "border: 1px solid #dee2e6; border-width: 1px; margin-bottom: 10px;", "aria-controls": "datatable"})
    )
    TipoEmpleado = forms.ChoiceField(
        choices = TIPO_EMPLEADO,
        label="Tipo de empleado",
        required=True,
        widget=forms.Select(attrs={"aria-controls": "datatable", "class": "form-control-sm", "style": "margin-bottom: 10px; border: 1px solid #dee2e6;"})
        )
    Nombres = forms.CharField(
        max_length=50,
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nombre(s)...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
        )
    ApellidoPaterno = forms.CharField(
        max_length=50,
        label="Apellido Paterno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "ApellidoPaterno...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
        )
    ApellidoMaterno = forms.CharField(
        max_length=50,
        label="Apellido Materno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "ApellidoMaterno...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px; margin-bottom: 10px;", "aria-controls": "datatable"}))
    Genero = forms.ChoiceField(
        choices = GENERO,
        label="Género",
        required=True,
        widget=forms.Select(attrs={"aria-controls": "datatable", "class": "form-control-sm", "style": "margin-bottom: 10px; border: 1px solid #dee2e6;"})
        )
    Nacimiento = forms.DateField(
        required=True,
        label="Fecha de nacimiento",
        widget=forms.widgets.DateInput(attrs={'type': 'date', "class": "form-control-sm", "style": "margin-bottom: 5px; border: 1px solid #dee2e6;"})
        )
    email = forms.EmailField(
        max_length=50,
        label="Correo electrónico",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "ejemplo@dominio.com...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
        )
    Telefono = forms.CharField(
        max_length=10,
        label="Telefono",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "0000000000...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
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
        Usuario = super(EditarUsuarioForm, self).save(commit=False)
        Usuario.set_password(self.cleaned_data["password1"])
        if commit:
            Usuario.save()
        return Usuario

class ExpedientePacienteForm(forms.ModelForm):
    Nombres = forms.CharField(
        max_length=50,
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nombre(s)", "class": "form-control"})
        )
    ApellidoPaterno = forms.CharField(
        max_length=50,
        label="Apellido Paterno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Apellido Paterno", "class": "form-control"}))
    ApellidoMaterno = forms.CharField(
        max_length=50,
        label="Apellido Materno",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Apellido Materno", "class": "form-control"}))
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
        widget=forms.TextInput(attrs={"placeholder": "Dirección", "class": "form-control"}))
    Correo = forms.EmailField(
        max_length=50,
        label="Correo electrónico",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "correo@sitio.com", "class": "form-control"}))
    Telefono = forms.CharField(
        max_length=10,
        label="Telefono",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Telefono", "class": "form-control"})
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
        widget=forms.Textarea(attrs={"placeholder": "Descripción de padecimientos del paciente.", "class": "form-control"})
        )
    class Meta:
        model = ExpedientePaciente
        fields = "__all__"
        exclude = ["FechaCreacion"]

class FiltroPacientes(Form):
    FILTER_CHOICES = (
        ("all", 'Todo los campos'),
        ("Nombres", 'Nombres'),
        ("Telefono", 'Telefono'),
        ("Correo", 'Correo'),
    )
    search = forms.CharField(required=False)
    filter_field = forms.ChoiceField(choices=FILTER_CHOICES)

class EditarPacienteForm(forms.ModelForm):
    Nombres = forms.CharField(
        max_length=50,
        label="Nombres",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Avellano", "class": "form-control"})
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
        label="Fecha de nacimiento")
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
    Nota = forms.CharField(
        max_length=200,
        label="Contenido de la nota del paciente",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Nota sobre el paciente.", "class": "form-control"})
        )
    class Meta:
        model = Nota
        fields = "__all__"
        exclude = ["FechaCreacion, Expedientepaciente"]

class FiltroTratamientos(Form):
    search = forms.CharField(required=False)

class TratamientoForm(forms.ModelForm):
    Tratamiento = forms.CharField(
        max_length=50,
        label="Nombre del tratamiento",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Tratamiento...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
        )
    Descripcion = forms.CharField(
        max_length=200,
        label="Descripción del tratamiento",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Nombre(s)...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
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
        widget=forms.TextInput(attrs={"placeholder": "Tratamiento...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
        )
    Descripcion = forms.CharField(
        max_length=200,
        label="Descripción del tratamiento",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Nombre(s)...", "class": "form-control form-control-sm", "style": "display: inline; border: 1px solid #dee2e6; border-width: 1px;", "aria-controls": "datatable"})
        )
    class Meta:
        model = Tratamiento
        fields = "__all__"
        exclude = []

class FiltroDoctores(Form):
    FILTER_CHOICES = (
        ("all", 'Todo los campos'),
        ("Nombres", 'Nombres'),
        ("Especialidad", 'Especialidad'),
        ("Correo", 'Correo'),
        ("Telefono", 'Telefono'),
    )
    search = forms.CharField(required=False)
    filter_field = forms.ChoiceField(choices=FILTER_CHOICES)

class DoctorForm(forms.ModelForm):
    Usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Doctor",
        required=True,
        )
    class Meta:
        model = Doctor
        fields = "__all__"
        exclude = []

class PerfilDoctorForm(forms.ModelForm):
    Tratamientos = forms.ModelMultipleChoiceField(
            queryset=Tratamiento.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)
    class Meta:
        model = Doctor
        fields = "__all__"
        exclude = ["Usuario"]


'''
Buscar como hacer eventos para hacer los queries de las horas y
tratamientos del Doctor cuando se selecciona el doctor
'''

class FiltroCitas(Form):
    FILTER_CHOICES = (
        ("all", 'Todo los campos'),
        ("Paciente", 'Doctor'),
        ("Doctor", 'Doctor'),
        ("Fecha", 'Fecha'),
    )
    search = forms.CharField(required=False)
    filter_field = forms.ChoiceField(choices=FILTER_CHOICES)

class CitaForm(forms.ModelForm):
    ExpedientePaciente = forms.ModelChoiceField(
        queryset=ExpedientePaciente.objects.all(),
        label="Paciente",
        required=True)
    Fecha = forms.DateField(
        required=True,
        label="Fecha de la cita",
        widget=forms.DateInput(format='%d/%m/%Y',attrs={'type': 'date'}))
    '''HoraInicio = forms.ChoiceField(
        label="Hora de Inicio",
        required=True)'''
    class Meta:
        model = Cita
        fields = "__all__"
        exclude = ["FechaCreacion"]

class EditarCitaForm(forms.ModelForm):
    ExpedientePaciente = forms.ModelChoiceField(
        queryset=ExpedientePaciente.objects.all(),
        label="Paciente",
        required=True)
    Fecha = forms.DateField(
        required=True,
        label="Fecha de la cita")
    '''HoraInicio = forms.ChoiceField(
        label="Hora de Inicio",
        required=True)'''
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

class EditarHoraForms(forms.ModelForm):
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
