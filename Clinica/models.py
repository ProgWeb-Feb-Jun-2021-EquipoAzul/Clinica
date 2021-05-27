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

    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(Usuario, self).save(*args, **kwargs)
        if is_new and self.TipoEmpleado =='D':
            doctor = Doctor(Usuario=self)
            doctor.save()

    def __str__(self):
        return self.Nombres + " " +self.ApellidoPaterno


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
        return self.Nombres + " " +self.ApellidoPaterno

class Nota(models.Model):
    Expedientepaciente= models.ForeignKey(ExpedientePaciente, verbose_name="Expediente del paciente", on_delete=models.RESTRICT)
    Nota = models.CharField(max_length=200, verbose_name="Nota")
    FechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Nota

class Tratamiento(models.Model):
    Tratamiento = models.CharField(max_length=50, verbose_name="Tratamiento")
    Descripcion = models.CharField(max_length=200, verbose_name="Descripcion")

    def __str__(self):
        return self.Tratamiento

class Doctor(models.Model):
    Usuario= models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.RESTRICT)
    Especialidad = models.CharField(null=True,blank=True,max_length=60, verbose_name="Especialidad")
    Tratamientos = models.ManyToManyField(Tratamiento, through='Doctor_Tratamiento')

    def __str__(self):
        return self.Usuario.Nombres + " " +self.Usuario.ApellidoPaterno

class Doctor_Tratamiento(models.Model):
    Doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.CASCADE)
    Tratamiento= models.ForeignKey(Tratamiento, verbose_name="Tratamiento", on_delete=models.CASCADE)

class Cita(models.Model):
    ExpedientePaciente= models.ForeignKey(ExpedientePaciente, verbose_name="Expediente del paciente", on_delete=models.RESTRICT)
    Doctor =models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.RESTRICT)
    Fecha= models.DateField(verbose_name="Fecha")
    HoraInicio = models.TimeField()
    HoraFin = models.TimeField()
    Tratamiento = models.CharField(max_length=50, verbose_name="Tratamiento")
    FechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Tratamiento

class Hora(models.Model):
    Dia =  models.DateField()
    Hora = models.TimeField()

    def __str__(self):
        return self.Dia

class Doctor_Hora(models.Model):
    Doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.RESTRICT)
    Hora= models.ForeignKey(Hora, verbose_name="Hora", on_delete=models.RESTRICT)
