from django.db import models
from Paciente.models import Paciente
from Doctor.models import Doctor,Especialidad,Habitacion

class Cita(models.Model):
    Estado_CITA = [
        ('programada','Programada'),
        ('Confirmada','Confirmada'),
        ('completada','Completada'),
        ('cancelada','Cancelada')
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=Estado_CITA, default='Programada')
    motivo = models.TextField()
    notas = models.TextField(blank=True)

class Ingreso(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField()
    fecha_alta = models.DateTimeField(null=True, blank=True)
    motivo = models.TextField()
    doctor_tratante = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class Factura(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagada = models.BooleanField(default=False)
    metodo_pago = models.CharField(max_length=50, blank=True) 


