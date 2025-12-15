from rest_framework import serializers
from .models import Paciente, HistorialMedico

class PacienteSerializer(serializers.ModelSerializer):
   class Meta:
      model = Paciente
      fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento', 'cedula', 'direccion', 'tipo_sangre', 'alergias', 'fecha_Registro']

class HistorialSerializer(serializers.ModelSerializer):
   class Meta:
      model = HistorialMedico
      fields = ['paciente', 'doctor', 'fecha_consulta', 'diagnostico', 'Tratamiento', 'observaciones']