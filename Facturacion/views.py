from django.shortcuts import render, redirect
from .models import Cita, Ingreso, Factura
from .serializers import CitaSerializer, IngresoSerializer, FacturaSerializer
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from .models import Cita, Ingreso, Factura, Doctor, Especialidad

class CitaCreate(generics.ListCreateAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

class CitaDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

class IngresoCreate(generics.ListCreateAPIView):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer

class IngresoDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer

class FacturaCreate(generics.ListCreateAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer 

class FacturaDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

def cliente_dashboard(request):
    citas = Cita.objects.all()
    ingresos = Ingreso.objects.all()
    facturas = Factura.objects.all()

    contexto = {
        'citas': citas,
        'ingresos': ingresos,
        'facturas': facturas,
    }
    return render(request, 'Cliente/ClienteDashboard.html', contexto)

@login_required
def crear_cita(request):
    if request.method == "POST":
        paciente = request.user.paciente
        doctor_id = request.POST.get("doctor")
        especialidad_id = request.POST.get("especialidad")
        fecha_hora = request.POST.get("fecha_hora")
        motivo = request.POST.get("motivo")

        doctor = Doctor.objects.get(id=doctor_id)
        especialidad = Especialidad.objects.get(id=especialidad_id)

        Cita.objects.create(
            paciente=paciente,
            doctor=doctor,
            Especialidad=especialidad,
            fecha_hora=fecha_hora,
            motivo=motivo
        )
    return redirect('cliente_dashboard')  # Redirige al dashboard

@login_required
def crear_ingreso(request):
    if request.method == "POST":
        paciente = request.user.paciente
        habitacion_id = request.POST.get("habitacion")
        doctor_id = request.POST.get("doctor")
        motivo = request.POST.get("motivo")

        habitacion = Habitacion.objects.get(id=habitacion_id)
        doctor = Doctor.objects.get(id=doctor_id)

        Ingreso.objects.create(
            paciente=paciente,
            habitacion=habitacion,
            fecha_ingreso=timezone.now(),  # o puedes usar un input si quieres
            doctor_tratante=doctor,
            motivo=motivo
        )
    return redirect('cliente_dashboard')