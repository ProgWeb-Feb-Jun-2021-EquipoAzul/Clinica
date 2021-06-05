from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

username_validator = UnicodeUsernameValidator()

TIPO_EMPLEADO = (
        ('A', 'Administrador'),
        ('R', 'Recepcionista'),
        ('D', 'Doctor'),
    )

GENERO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

DIA = (
        ('Domingo', 'Domingo'),
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miercoles', 'Miercoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sabado', 'Sabado'),
    )

GENERO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )

class Usuario(AbstractUser):
    username = models.CharField(
        max_length=50,
        verbose_name="Usuario",
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    TipoEmpleado = models.CharField(max_length=1,choices=TIPO_EMPLEADO, verbose_name="Tipo de empleado",default='A')
    Nombres = models.CharField(max_length=50, verbose_name="Nombres",blank=True)
    ApellidoPaterno = models.CharField(max_length=50,verbose_name="Apellido paterno",blank=True)
    ApellidoMaterno = models.CharField(max_length=50,verbose_name="Apellido materno",blank=True)
    Genero = models.CharField(max_length=1,choices=GENERO,verbose_name="Género",blank=True)
    Nacimiento= models.DateField(verbose_name="Fecha de nacimiento",blank=True, null=True)
    email = models.EmailField(max_length=50,verbose_name="Correo electrónico", blank=True)
    Telefono = models.CharField(max_length=12,verbose_name="Telefono",null=True)
    date_joined = models.DateTimeField(verbose_name="Fecha de creacion",auto_now_add=True)



    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(Usuario, self).save(*args, **kwargs)
        if is_new and self.TipoEmpleado =='D':
            doctor = Doctor(Usuario=self)
            doctor.save()

    def __str__(self):
        return self.Nombres + " " +self.ApellidoPaterno

'''class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    models.CharField(max_length=1,choices=TIPO_EMPLEADO, verbose_name="Tipo de empleado")
    Nombres = models.CharField(max_length=50, verbose_name="Nombres")
    ApellidoPaterno = models.CharField(max_length=50,verbose_name="Apellido paterno")
    ApellidoMaterno = models.CharField(max_length=50,verbose_name="Apellido materno")
    Genero = models.CharField(max_length=1,choices=GENERO,verbose_name="Género")
    Nacimiento= models.DateField(verbose_name="Fecha de nacimiento")
    Correo = models.EmailField(max_length=50,verbose_name="Correo electrónico")
    Telefono = models.CharField(max_length=12,verbose_name="Telefono")

    def __str__(self):
        return self.Nombres + " " +self.ApellidoPaterno'''

'''def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        n = Usuario.objects.create(user=instance)
    if instance.TipoEmpleado == 'D':
        Doctor.objects.create(Usuario=n)
post_save.connect(post_user_created_signal, sender=User)'''


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
    ##Fechaupdate

    def __str__(self):
        return self.Nombres + " " +self.ApellidoPaterno

class Nota(models.Model):
    Expedientepaciente= models.OneToOneField(ExpedientePaciente, verbose_name="Expediente del paciente", on_delete=models.RESTRICT)
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
    Usuario= models.OneToOneField(Usuario, on_delete=models.CASCADE)
    Especialidad = models.CharField(null=True,blank=True,max_length=60, verbose_name="Especialidad")
    Tratamientos = models.ManyToManyField(Tratamiento, through='Clinica.Doctor_Tratamiento')

    def __str__(self):
        return self.Usuario.Nombres + " " +self.Usuario.ApellidoPaterno

class Hora(models.Model):
    Doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.CASCADE)
    Dia =  models.CharField(max_length=10,choices=DIA,verbose_name="Género",blank=True)
    Hora = models.TimeField()
    class Meta:
        unique_together = ('Doctor','Dia', 'Hora')

    def __str__(self):
        return self.Dia + " " + self.Hora.strftime("%H:%M")


'''
class Doctor_Hora(models.Model):
    Doctor= models.ForeignKey(Doctor, verbose_name="Doctor", on_delete=models.RESTRICT)
    Hora= models.ForeignKey(Hora, verbose_name="Hora", on_delete=models.RESTRICT)'''

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
