from rest_framework import serializers
from .models import Cita, Ingreso, Factura

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
      model = Cita
      fields = ['paciente', 'doctor', 'Especialidad', 'fecha_hora', 'estado', 'motivo', 'notas']
    
class IngresoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Ingreso
      fields = ['paciente', 'habitacion', 'fecha_ingreso', 'fecha_alta', 'motivo', 'doctor_tratante']

class FacturaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Factura
      fields = ['paciente', 'fecha_emision', 'subtotal', 'iva', 'total', 'pagada', 'metodo_pago']