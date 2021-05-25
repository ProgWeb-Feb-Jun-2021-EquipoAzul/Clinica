from django.db import models

# Create your models here.

TIPO_EMPLEADO = (
        ('A', 'Administrador'),
        ('R', 'Recepcionista'),
        ('D', 'Doctor'),
    )

GENERO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

class Usuario(models.Model):
    NombreUsuario = models.CharField(max_length=30, verbose_name="Cuenta del usuario")
    Contrasena = models.CharField(max_length=50, verbose_name="Contraseña")
    TipoEmpleado = models.CharField(max_length=1,choices=TIPO_EMPLEADO, verbose_name="Tipo de empleado")
    Nombres = models.CharField(max_length=50, verbose_name="Nombres")
    ApellidoPaterno = models.CharField(max_length=50,verbose_name="Apellido paterno")
    ApellidoMaterno = models.CharField(max_length=50,verbose_name="Apellido materno")
    Genero = models.CharField(max_length=1,choices=GENERO,verbose_name="Género")
    Nacimiento= models.DateField(verbose_name="Fecha de nacimiento")
    Correo = models.EmailField(max_length=50,verbose_name="Correo electrónico")
    Telefono = models.CharField(max_length=12,verbose_name="Telefono")
    UltimoAcceso = models.DateTimeField(auto_now_add=True, verbose_name="Ultimo acceso al sistema")

    def __str__(self):
        return self.Nombre + " " +self.ApellidoPaterno


class ExpedientePaciente(models.Model):
    Nombres = models.CharField(max_length=50, verbose_name="Nombres")
    ApellidoPaterno = models.CharField(max_length=50,verbose_name="Apellido paterno")
    ApellidoMaterno = models.CharField(max_length=50,verbose_name="Apellido materno")
    Genero = models.CharField(max_length=1,choices=GENERO,verbose_name="Género")
    Nacimiento= models.DateField(verbose_name="Fecha de nacimiento")
    Direccion = models.CharField(max_length=80, verbose_name="Direccion")
    Correo = models.EmailField(max_length=50,verbose_name="Correo electrónico")
    Telefono = models.CharField(max_length=12,verbose_name="Telefono")
    Alergias = models.CharField(max_length=200, verbose_name="Alergias")
    Padecimientos = models.CharField(max_length=200, verbose_name="Padecimientos")
    FechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Nombre + " " +self.ApellidoPaterno

class Doctor(models.Model):
    usuario= models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.RESTRICT)
    Especialidad = models.CharField(max_length=50, verbose_name="Especialidad")





    def __str__(self):
        return self.Especialidad

class Nota(models.Model):
    Nota = models.CharField(max_length=50, verbose_name="Nota")
    FechaCreacion = models.DateTimeField()


    def __str__(self):
        return self.Nota

class Expediente_Nota(models.Model):
    expedientepaciente= models.ForeignKey(ExpedientePaciente, verbose_name="Expediente del paciente", on_delete=models.RESTRICT)
    nota= models.ForeignKey(Nota, verbose_name="Nota", on_delete=models.RESTRICT)



class Cita(models.Model):
    expedientepaciente= models.ForeignKey(ExpedientePaciente, verbose_name="Expediente del paciente", on_delete=models.RESTRICT)
    doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.RESTRICT)
    Fecha =  models.DateField()
    HoraInicio = models.TimeField()
    HoraFin = models.TimeField()
    Tratamiento = models.CharField(max_length=50, verbose_name="Tratamiento")
    FechaCreacion = models.DateTimeField()

    def __str__(self):
        return self.Tratamiento

class Tratamiento(models.Model):
    Tratamiento = models.CharField(max_length=50, verbose_name="Tratamiento")
    Descripcion = models.CharField(max_length=50, verbose_name="Descripcion")

    def __str__(self):
        return self.Tratamiento


class Doctor_Tratamiento(models.Model):
    doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.RESTRICT)
    tratamiento= models.ForeignKey(Tratamiento, verbose_name="Tratamiento", on_delete=models.RESTRICT)



class Hora(models.Model):
    Dia =  models.DateField()
    Hora = models.TimeField()


    def __str__(self):
        return self.Dia

class Doctor_Hora(models.Model):
    doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.RESTRICT)
    hora= models.ForeignKey(Hora, verbose_name="Hora", on_delete=models.RESTRICT)
