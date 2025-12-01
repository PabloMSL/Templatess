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
    
    
def farmacia_dashboard(request):
    medicamentos = Medicamento.objects.all()
    recetas = Receta.objects.all()

    contexto = {
        'medicamentos': medicamentos,
        'recetas': recetas
    }
    return render(request, 'Medicamento/FarmaciaDashboard.html', contexto)