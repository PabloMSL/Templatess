from django.db import models
from Doctor.models import Doctor

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()
    tipo_sangre = models.CharField(max_length=5)
    alergias = models.TextField(blank=True)
    fecha_Registro = models.DateTimeField(auto_now_add=True)

class HistorialMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField()
    Tratamiento = models.TextField()
    observaciones = models.TextField(blank=True)