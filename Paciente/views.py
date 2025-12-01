from django.shortcuts import render
from .models import Paciente, HistorialMedico
from .serializers import PacienteSerializer, HistorialSerializer
from rest_framework import generics

class PacienteCreate(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer 

class PacienteDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class HistorialCreate(generics.ListCreateAPIView):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialSerializer

class HistorialDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialSerializer

