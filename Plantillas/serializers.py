from Plantillas.models import monito
from rest_framework import serializers

class monitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = monito
        fields = '__all__'