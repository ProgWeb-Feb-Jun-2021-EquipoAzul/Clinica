from django.db import models

# Create your models here.


# Create your models here.

class TipoEmpleado(models.Model):
    Tipo = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Tipo

class Usuario(models.Model):
    tipoempleado= models.ForeignKey(TipoEmpleado, verbose_name="TipoEmpleado", on_delete=models.RESTRICT)
    Nombre = models.CharField(max_length=50, verbose_name="Nombre")
    ApellidoPaterno = models.CharField(max_length=50,verbose_name="Apellido Paterno")
    ApellidoMaterno = models.CharField(max_length=50,verbose_name="Apellido Materno")
    UltimoAcceso = models.DateTimeField()
    Genero = models.CharField(max_length=10,verbose_name="Genero")
    Nacimiento= models.DateField()
    Correo = models.EmailField()
    Telefono = models.CharField(max_length=50, verbose_name="Telefono")

    def __str__(self):
        return self.Nombre + " " +self.Apellido


class ExpedientePaciente(models.Model):
    Nombre = models.CharField(max_length=50,  verbose_name="Nombre")
    ApellidoPaterno = models.CharField(max_length=50,verbose_name="Apellido Paterno")
    ApellidoMaterno = models.CharField(max_length=50,verbose_name="Apellido Materno")
    Correo = models.EmailField()
    Genero = models.CharField(max_length=10,verbose_name="Genero")
    Telefono = models.CharField(max_length=50, verbose_name="Telefono")
    Direccion = models.CharField(max_length=50, verbose_name="Direccion")
    Nacimiento= models.DateField()
    Correo = models.EmailField()
    Alergias = models.CharField(max_length=50, verbose_name="Alergias")
    Padecimientos = models.CharField(max_length=50, verbose_name="Padecimientos")
    FechaCreacion = models.DateTimeField()

    def __str__(self):
        return self.Nombre + " " +self.Apellido

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
    
