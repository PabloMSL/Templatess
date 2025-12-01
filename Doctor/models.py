from django.db import models

class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_Contratacion = models.DateField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_consulta = models.IntegerField(help_text="Duracion en minutos")

class Habitacion(models.Model):
    TIPO_HABITACION = [
        ('individual', 'Individual'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
        ('uci', 'UCI')
    ]
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_HABITACION)
    piso = models.IntegerField()
    disponible = models.BooleanField(default=True)
    costo_diario = models.DecimalField(max_digits=10, decimal_places=2)
