from django.shortcuts import render
from Plantillas.models import monito
from Plantillas.serializers import monitoSerializer
from rest_framework import generics

class monitocreate(generics.ListCreateAPIView):
    queryset = (monito.objects.all),
    serializer_class = monitoSerializer
    
class monitodestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = (monito.objects.all),
    serializer_class = monitoSerializer

def inicio(request):
    contexto = {
        "nombre_museo": "Museo de Arte Moderno",
        "descripcion": "Un espacio dedicado a las expresiones artísticas contemporáneas.",
        "abierto": True,
        "imagenes": [
            "img/expo1.png",
            "img/expo2.jpg",
            "img/expo3.jpg",
            "img/expo4.jpg",
            "img/expo5.jpg",
            "img/expo6.jpg",
        ],
    }
    return render(request, "Plantillas/inicio.html", contexto)

