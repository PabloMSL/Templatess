from django.shortcuts import render
from .models import Medicamento, Receta
from .serializers import MedicamentoSerializer, RecetaSerializer
from rest_framework import generics

class MedicamentoCreate(generics.ListCreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class MedicamentoDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class RecetaCreate(generics.ListCreateAPIView):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer

class RecetaDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer 