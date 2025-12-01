from rest_framework import serializers
from .models import Medicamento, Receta

class MedicamentoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Medicamento
      fields = ['nombre', 'descripcion', 'laboratorio', 'precio', 'stock', 'requiere_receta']

class RecetaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Receta
      fields = ['historial', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones']