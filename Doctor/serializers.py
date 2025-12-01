from rest_framework import serializers
from .models import Doctor, Habitacion, Especialidad

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
     model = Doctor
     fields = ['nombre', 'email', 'telefono', 'cedula', 'fecha_Contratacion', 'activo']

class HabitacionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Habitacion
      fields = ['numero', 'tipo', 'piso', 'disponible', 'costo_diario']

class EspecialidadSerializer(serializers.ModelSerializer):
   class Meta:
      model = Especialidad
      fields = ['nombre', 'descripcion', 'duracion_consulta']